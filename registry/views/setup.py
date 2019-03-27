import stripe

from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from alumni.models import Approval
from alumni.fields import PaymentTypeField
from registry.decorators import require_unset_component
from registry.views.registry import default_alternative
from ..forms import RegistrationForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, SkillsForm, AtlasSettingsForm

from django.core.exceptions import ObjectDoesNotExist

def register(request):
    """ Implements the new Alumni Registration Page"""

    # not for already logged in users
    if request.user.is_authenticated:
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

        # check if the user is approved
        try:
            approved = request.user.alumni.approval.approval
        except ObjectDoesNotExist:
            approved = False

        # If the user is not approved, show him that he finished the setup
        if not approved:
            return render(request, 'setup/finished.html', {'user': request.user})
        # else go straight to the portal
        else:
            return redirect(reverse('portal'))

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
atlas = setupViewFactory('atlas', AtlasSettingsForm, 'Atlas Setup', 'A Map & Search Interface for Alumni')

