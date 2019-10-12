from payments import stripewrapper

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import formats
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from .forms import MembershipInformationForm, PaymentMethodForm
from .models import SubscriptionInformation
from .plans import subscription_plans

from registry.decorators import require_setup_completed
from registry.views.setup import SetupComponentView


class SignupView(SetupComponentView):
    setup_name = 'Tier Selection'
    setup_subtitle = 'How much do you want to support us?'
    setup_form_class = MembershipInformationForm

    template_name = 'payments/tier.html'

    def get_context(self, form):
        context = super().get_context(form)
        context['confirm_text'] = 'Confirm Membership'
        return context

    def form_valid(self, form):

        # Create the stripe customer
        customer, err = stripewrapper.create_customer(self.request.user.alumni)
        if err is not None:
            form.add_error(
                None, 'Something went wrong when talking to our payment service provider. Please try again later or contact support. ')
            return None

        # store the information
        instance = form.save(commit=False)
        instance.member = self.request.user.alumni
        instance.customer = customer.id
        instance.save()

        # if we selected the starter tier, create subscription information now
        if instance.tier == 'st':
            SubscriptionInformation.create_starter_subscription(
                self.request.user.alumni)

        return instance


class SubscribeView(SetupComponentView):
    setup_name = 'Payment Information'
    setup_subtitle = ''
    setup_form_class = PaymentMethodForm
    setup_next_text = 'CONFIRM MEMBERSHIP & AUTHORIZE PAYMENT NOW'

    template_name = 'payments/subscribe.html'

    @classmethod
    def setup_class(cls):
        return SubscriptionInformation

    def form_valid(self, form):
        # Attach the payment source to the customer
        customer = self.request.user.alumni.membership.customer
        _, err = form.attach_to_customer(customer)

        # if the error is not, return
        if err is not None:
            form.add_error(
                None, 'Something went wrong when talking to our payment service provider. Please try again later or contact support. ')
            return None

        # grab tier and plan
        tier = self.request.user.alumni.membership.tier
        plan = subscription_plans[tier].stripe_id

        # create a subscription on the plan
        sub, err = stripewrapper.create_subscription(customer, plan)
        if err is not None:
            form.add_error(
                None, 'Something went wrong trying to create the subscription. Please try again later or contact support. ')
            return None

        # Create the object
        instance = SubscriptionInformation.objects.create(
            member=self.request.user.alumni,
            tier=tier,
            subscription=sub.id,
            start=timezone.now()
        )

        return instance


@method_decorator(require_setup_completed, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.alumni.can_update_payment), name='dispatch')
class UpdatePaymentView(FormView):
    template_name = 'payments/subscribe.html'
    form_class = PaymentMethodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Update Payment Information',
            'updating': True,
            'next_text': 'AUTHORIZE PAYMENT NOW'
        })
        return context

    def form_valid(self, form):
        # Attach the payment source to the customer
        customer = self.request.user.alumni.membership.customer
        _, err = form.attach_to_customer(customer)

        # if the error is not, return
        if err is not None:
            form.add_error(
                None, 'Something went wrong when talking to our payment service provider. Please try again later or contact support. ')
            return None

        messages.success(self.request, 'Payment method has been updated. ')

        return self.form_invalid(form)


class PaymentsTableMixin:
    @classmethod
    def format_datetime(cls, epoch, format="DATETIME_FORMAT"):
        """ Formats seconds since epoch as a readable date """
        date_joined = datetime.fromtimestamp(epoch)
        return formats.date_format(date_joined, format)

    @classmethod
    def format_description(cls, line):
        """ Formats the description line of an invoice """
        # if we have a description, return it
        if line.description is not None:
            return line.description

        # if we have a subscription show {{Name}} x timeframe
        if line.type == "subscription":
            name = "{} ({} - {})".format(line.plan.name,
                                         cls.format_datetime(line.period.start,
                                                             "DATE_FORMAT"),
                                         cls.format_datetime(line.period.end,
                                                             "DATE_FORMAT"))
            return "{} x {}".format(line.quantity, name)

        # we have a normal line item, and there should have been a description
        else:
            raise Exception("Non-subscription without description")

    @classmethod
    def format_total(cls, amount, cur):
        """ Formats the total """
        if cur == "eur":
            return "%0.2f €" % (amount / 100)
        elif cur == "usd":
            return "%0.2f $" % (amount / 100)
        else:
            raise Exception("unknown currency {}".format(cur))

    @classmethod
    def get_invoice_table(cls, customer):
        invoices, err = stripewrapper.get_payment_table(customer)
        described = []

        if err is None:
            try:
                invoices = [{
                    'lines': [cls.format_description(l) for l in iv['lines']],
                    'date': cls.format_datetime(iv['date']),
                    'total': cls.format_total(iv['total'][0], iv['total'][1]),
                    'paid': iv['paid'],
                    'closed': iv['closed']
                } for iv in invoices]
            except Exception as e:
                err = e
        else:
            err = 'Something went wrong. Please try again later or contact support. '

        return invoices, err

    @classmethod
    def format_method(cls, source):
        if source['kind'] == 'card':
            return '{} Card ending in {} (valid until {}/{})'.format(source['brand'], source['last4'], source['exp_month'], source['exp_year'])
        elif source['kind'] == 'sepa':
            return 'Bank Account ending in {} (<a href="{}" target="_blank">SEPA Mandate Reference {}</a>)'.format(source['last4'], source['mandate_url'], source['mandate_reference'])
        else:
            return 'Unknown Payment Method. Please contact support. '

    @classmethod
    def get_method_table(cls, customer):
        methods, err = stripewrapper.get_methods_table(customer)
        if err is None:
            methods = [cls.format_method(method) for method in methods]
        else:
            err = 'Something went wrong. Please try again later or contact support. '

        return methods, err


@method_decorator(require_setup_completed, name='dispatch')
class PaymentsView(PaymentsTableMixin, TemplateView):
    template_name = 'payments/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer = self.request.user.alumni.membership.customer
        context['user'] = self.request.user

        invoices, error = self.__class__.get_invoice_table(customer)
        context['invoices'] = invoices

        if error is None:
            methods, error = self.__class__.get_method_table(customer)
            context['methods'] = methods

        context['error'] = error

        return context
