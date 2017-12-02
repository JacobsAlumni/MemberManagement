from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from registry.views.registry import default_alternative
from ..decorators import require_setup_completed

from ..forms import AlumniForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, PaymentInformationForm


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
            messages.success(request, 'Your password was successfully updated!')
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

