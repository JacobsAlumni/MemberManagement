from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect

from ..forms import AlumniForm, AddressForm, JacobsForm, SocialMediaForm, \
    JobInformationForm, PaymentInformationForm


def editViewFactory(prop, FormClass, name):
    """ Generates an edit view for a given section of the profile """

    @login_required
    def edit(request):

        # if we have something that needs to be setup return to the main page
        if request.user.alumni.get_first_unset_approval() is not None:
            return redirect(reverse('portal'))

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

                # and then continue to the main portal page.
                return redirect(url)

        # if we did not have any post data, simply create a new form
        else:
            form = FormClass(instance=instance)

        # and return the request
        return render(request, 'portal/edit.html',
                      {'form': form, 'name': name})

    return edit


edit = editViewFactory(None, AlumniForm, 'General Information')
address = editViewFactory('address', AddressForm, 'Address')
jacobs = editViewFactory('jacobs', JacobsForm, 'Jacobs Data')
social = editViewFactory('social', SocialMediaForm, 'Social Media')
job = editViewFactory('job', JobInformationForm, 'Job Information')
payment = editViewFactory('payment', PaymentInformationForm, 'Payment Information')