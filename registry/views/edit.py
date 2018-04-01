from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings

from raven.contrib.django.raven_compat.models import client

from registry.views.registry import default_alternative
from ..decorators import require_setup_completed

from ..forms import AlumniForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, PaymentInformationForm, SkillsForm

import stripe


def editViewFactory(prop, FormClass, name):
    """ Generates an edit view for a given section of the profile """

    @require_setup_completed(default_alternative)
    def edit(request):

        # figure out the edit url to redirect to
        if prop is None:
            url = reverse('edit')
        else:
            url = reverse('edit_{}'.format(prop))

        # load the instance
        if prop is None:
            instance = request.user.alumni
        else:
            instance = getattr(request.user.alumni, prop)

        if request.method == 'POST':
            # load the form
            form = FormClass(request.POST, instance=instance)

            # check that the form is valid
            if form.is_valid():
                form.clean()

                # Create the Address form
                instance = form.save(commit=False)
                instance.save()

                # Add a success message
                messages.success(request, 'Changes saved. ')

                # and then continue to the main portal page.
                return redirect(url)

        # if we did not have any post data, simply create a new form
        else:
            form = FormClass(instance=instance)

        # and return the request
        return render(request, 'portal/edit.html',
                      {
                          'form': form,
                          'name': name,
                          'messsages': get_messages(request)
                      })

    return edit


edit = editViewFactory(None, AlumniForm, 'General Information')
address = editViewFactory('address', AddressForm, 'Address')
jacobs = editViewFactory('jacobs', JacobsForm, 'Jacobs Data')
social = editViewFactory('social', SocialMediaForm, 'Social Media')
job = editViewFactory('job', JobInformationForm, 'Job Information')
skills = editViewFactory('skills', SkillsForm, 'Education and Skills')
payment = editViewFactory('payment', PaymentInformationForm,
                          'Payment Information')


@require_setup_completed(default_alternative)
def password(request):
    # if we have something that needs to be setup return to the main page
    if request.user.alumni.get_first_unset_component() is not None:
        return redirect(reverse('portal'))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('edit_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'portal/edit.html', {
        'form': form,
        'name': 'Password',
        'messsages': get_messages(request)
    })


@require_setup_completed(default_alternative)
def payments(request):
    error = None
    customer = None
    invoices = None

    customer_id = request.user.alumni.payment.customer

    if customer_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            customer = stripe.Customer.retrieve(customer_id)
            invoices = stripe.Invoice.list(customer=customer_id)
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

    return render(request, 'payments/view.html', {
        'customer': customer,
        'invoices': invoices,
        'error': error
    })
