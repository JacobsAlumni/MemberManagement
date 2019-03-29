import stripe
from datetime import datetime
from raven.contrib.django.raven_compat.models import client

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import formats
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from .forms import PaymentInformationForm
from .models import PaymentInformation
from .plans import subscription_plans

from alumni.fields import PaymentTypeField

from registry.decorators import require_setup_completed, require_unset_component
from registry.views.registry import default_alternative


@method_decorator(require_unset_component('payment', default_alternative), name='dispatch')
class SubscribeView(FormView):
    template_name = 'payments/subscribe.html'
    form_class = PaymentInformationForm
    success_url = reverse_lazy('portal')

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        context['publishable_key'] = stripe.publishable_key
        return context

    def form_valid(self, form):
        tier = form.cleaned_data['tier']
        customer_data = {
            'description': "Jacobs Alumni {} for {} ({})".format(subscription_plans[tier].name,
                                                                 self.request.user.alumni.fullName,
                                                                 self.request.user.alumni.email),
            'email': self.request.user.email,
        }
        ptype = form.cleaned_data['payment_type']

        if ptype == PaymentTypeField.SEPA:
            sepa_mandate = form.cleaned_data['sepa_mandate']
            customer_data['source'] = sepa_mandate['id']
        elif ptype == PaymentTypeField.CARD:
            customer_data["card"] = form.cleaned_data['token']
        else:
            return form.add_error(None,
                                  'Only credit cards, certain debit cards, and SEPA transfers are accepted at the moment')

        try:
            customer = stripe.Customer.create(**customer_data)
            subscription = customer.subscriptions.create(
                plan=subscription_plans[tier].stripe_id)
        except stripe.error.CardError as e:
            client.captureException()
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            form.add_error(None,
                           'Your card has been declined ({})'.format(
                               err.get('message')))
            return self.form_invalid(form)
        except stripe.error.RateLimitError as e:
            client.captureException()
            # Too many requests made to the API too quickly
            form.add_error(None,
                           'Unable to communicate with our service payment provider (stripe.error.RateLimitError). Please try again later or contact support. ')
            return self.form_invalid(form)
        except stripe.error.InvalidRequestError as e:
            print(e)
            client.captureException()
            # Invalid parameters were supplied to Stripe's API
            form.add_error(None,
                           'Unable to communicate with our service payment provider (stripe.error.InvalidRequestError). Please try again later or contact support. ')
            return self.form_invalid(form)
        except stripe.error.AuthenticationError as e:
            client.captureException()
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            form.add_error(None,
                           'Unable to communicate with our service payment provider (stripe.error.AuthenticationError). Please try again later or contact support. ')
            return self.form_invalid(form)
        except stripe.error.APIConnectionError as e:
            client.captureException()
            # Network communication with Stripe failed
            form.add_error(None,
                           'Unable to communicate with our service payment provider (stripe.error.APIConnectionError). Please try again later or contact support. ')
            return self.form_invalid(form)
        except stripe.error.StripeError as e:
            client.captureException()
            # Display a very generic error to the user, and maybe send
            # yourself an email
            form.add_error(None,
                           'Something went wrong trying to process your payment. Please try again later. ')
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, 'Something went wrong trying to process your payment. Please try again. ')
            return self.form_invalid(form)

        # Create an instance for the payment in the database
        instance = form.save(commit=False)
        instance.member = self.request.user.alumni
        instance.customer = customer.stripe_id
        instance.subscription = subscription.stripe_id

        # and save it
        instance.save()
        return super(SubscribeView, self).form_valid(form)


@method_decorator(require_setup_completed(default_alternative), name='dispatch')
class PaymentsView(TemplateView):
    template_name = 'payments/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        (error, invoices) = get_invoice_table(self.request.user.alumni.payment.customer)

        context.update({
            'invoices': invoices,
            'error': error
        })

        return context

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class PaymentsAdminView(TemplateView):
    template_name = 'payments/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        payment = get_object_or_404(PaymentInformation,
                                member__profile__id=kwargs['id'])

        (error, invoices) = get_invoice_table(payment.customer)

        context.update({
            'admin': True,
            'username': payment.member.profile.username,
            'invoices': invoices,
            'error': error
        })

        return context

def format_datetime(epoch, format="DATETIME_FORMAT"):
    """ Formats seconds since epoch as a readable date """

    date_joined = datetime.fromtimestamp(epoch)
    return formats.date_format(date_joined, format)


def format_total(amount, cur):
    """ Formats the total """
    if cur == "eur":
        return "%0.2f €" % (amount / 100)
    elif cur == "usd":
        return "%0.2f $" % (amount / 100)
    else:
        raise Exception("unknown currency {}".format(cur))


def format_description(line):
    """ Formats the description line of an invoice """

    # if we have a description, return it
    if line.description is not None:
        return line.description

    # if we have a subscription show {{Name}} x timeframe
    if line.type == "subscription":
        name = "{} ({} - {})".format(line.plan.name,
                                     format_datetime(line.period.start,
                                                     "DATE_FORMAT"),
                                     format_datetime(line.period.end,
                                                     "DATE_FORMAT"))
        return "{} x {}".format(line.quantity, name)

    # we have a normal line item, and there should have been a description
    else:
        raise Exception("Non-subscription without description")


def get_invoice_table(customer_id):
    error = None
    invoices = []

    if customer_id:
        try:
            for iv in stripe.Invoice.list(customer=customer_id):
                invoices.append({
                    'lines': [format_description(l) for l in iv.lines],
                    'date': format_datetime(iv.date),
                    'total': format_total(iv.total, iv.currency),
                    'paid': iv.paid,
                    'closed': iv.closed
                })
        except stripe.error.RateLimitError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.RateLimitError). " \
                    "Please try again later or contact support. "
        except stripe.error.InvalidRequestError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.InvalidRequestError). " \
                    "Please try again later or contact support. "
        except stripe.error.AuthenticationError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.AuthenticationError). " \
                    "Please try again later or contact support. "
        except stripe.error.APIConnectionError as e:
            client.captureException()
            error = "Unable to communicate with our service payment " \
                    "provider (stripe.error.APIConnectionError). " \
                    "Please try again later or contact support. "
        except stripe.error.StripeError as e:
            client.captureException()
            error = "Something went wrong trying to retrieve your payments. " \
                    "Please try again later or contact support. "
        except Exception as e:
            client.captureException()
            error = "Something went wrong trying to retrieve your payments. " \
                    "Please try again later or contact support. "
    else:
        error = "Something went wrong (missing Customer ID). " \
                "Please contact support or try again later. "

    return (error, invoices)