import stripe
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from registry.decorators import require_unset_component
from registry.models import subscription_plans
from registry.views.registry import default_alternative
from ..forms import RegistrationForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, PaymentInformationForm


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
            username, password = \
                form.cleaned_data['username'], form.cleaned_data['password1']
            user = User.objects.create_user(username, None, password=password)
            user.save()

            # Create the Alumni Data Object
            instance = form.save(commit=False)
            instance.profile = user
            instance.save()

            # Authenticate the user for this request
            login(request, user)

            # and then redirect the user to the main setup page
            return redirect(reverse('setup'))

    # if we did not have any post data, simply create a new form
    else:
        form = RegistrationForm()

    # and return the request
    return render(request, 'setup/setup.html', {
        'form': form,
        'title': 'Register -  Enter your General Information',
        'subtitle': 'just the basics',
        'next_text': 'Join the Alumni Association'
    })


@login_required
def setup(request):
    """ Generates a setup page according to the given component. """

    component = request.user.alumni.get_first_unset_component()

    # if we have finished everything, return the all done page
    if component is None:
        return render(request, 'setup/finished.html',
                      {'user': request.user})

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
                          'title': 'Initial Setup - {}'.format(name),
                          'subtitle': subtitle,
                          'next_text': 'Continue'
                      })

    return setup


address = setupViewFactory('address', AddressForm, 'Residential Address',
                           'so that we can contact you if needed')
jacobs = setupViewFactory('jacobs', JacobsForm, 'Alumni Data', 'tell us what you did at Jacobs')
social = setupViewFactory('social', SocialMediaForm, 'Social Media', '')
job = setupViewFactory('job', JobInformationForm, 'Job Information', '')


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
            'description': subscription_plans[tier].name,
            'card': form.cleaned_data['token']
        }
        customer = stripe.Customer.create(**customer_data)
        customer.subscriptions.create(plan=subscription_plans[tier].stripe_id)

        # store card_token
        # store cusp,ter_id
        # store subscription id

        return super(SubscribeView, self).form_valid(form)
