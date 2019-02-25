import stripe

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from raven.contrib.django.raven_compat.models import client

from alumni.models import Approval
from alumni.fields import PaymentTypeField
from registry.decorators import require_unset_component
from registry.models import subscription_plans
from registry.views.registry import default_alternative
from ..forms import RegistrationForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, PaymentInformationForm, SkillsForm


def register(request):
    """ Implements the new Alumni Registration Page"""

    # not for already logged in users
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        # load the form
        form = RegistrationForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # create a user object and save it
            username = form.cleaned_data['username']
            user = User.objects.create_user(username, None, password=None)
            user.save()

            # Create the Alumni Data Object
            instance = form.save(commit=False)
            instance.profile = user
            instance.save()

            # create an empty approval object
            approval = Approval(member=instance, approval=False, gsuite=None)
            approval.save()

            # Authenticate the user for this request
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # and then redirect the user to the main setup page
            return redirect(reverse('setup'))

    # if we did not have any post data, simply create a new form
    else:
        form = RegistrationForm()

    # and return the request
    return render(request, 'setup/setup.html', {
        'form': form,
        'title': 'Register',
        'subtitle': 'Enter your General Information - just the basics',
        'next_text': 'Continue Application'
    })


@login_required
def setup(request):
    """ Generates a setup page according to the given component. """

    component = request.user.alumni.get_first_unset_component()

    # if we have finished everything, return the all done page
    if component is None:
        return render(request, 'setup/finished.html', {'user': request.user})

    # else redirect to the setup page.
    else:
        return redirect(reverse('setup_{}'.format(component)))


def setupViewFactory(prop, FormClass, name, subtitle):
    """ Generates a setup view for a given section of the profile """

    @require_unset_component(prop, default_alternative)
    def setup(request):

        # reverse the url to redirect to
        url = reverse('setup')

        if request.method == 'POST':
            # load the form
            form = FormClass(request.POST)

            # check that the form is valid
            if form.is_valid():
                form.clean()

                # Create the data instance
                instance = form.save(commit=False)
                instance.member = request.user.alumni
                instance.save()

                # and then continue to the main setup page
                return redirect(url)

        # if we did not have any post data, simply create a new form
        else:
            form = FormClass()

        # and return the request
        return render(request, 'setup/setup.html',
                      {
                          'form': form,
                          'title': name,
                          'subtitle': subtitle,
                          'next_text': 'Continue'
                      })

    return setup


address = setupViewFactory('address', AddressForm,
                           'General Information - Residential Address', '')
social = setupViewFactory('social', SocialMediaForm, 'Social Media Data', '')
jacobs = setupViewFactory('jacobs', JacobsForm, 'Alumni Data',
                          'tell us what you did at Jacobs')
job = setupViewFactory('job', JobInformationForm, 'Professional information',
                       'What did you do after Jacobs?')
skills = setupViewFactory('skills', SkillsForm, 'Education and Skills', '')


class SubscribeView(FormView):
    template_name = 'payments/subscribe.html'
    form_class = PaymentInformationForm
    success_url = reverse_lazy('portal')
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_SECRET_KEY
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

    @classmethod
    def as_safe_view(cls, **initkwargs):
        dec = require_unset_component('payment', default_alternative)
        view = cls.as_view(**initkwargs)
        return dec(view)
