from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import AddressForm, JacobsForm, SocialMediaForm, JobInformationForm


@login_required
def setup(request):
    """ Generates a setup page according to the given component. """

    component = request.user.alumni.get_first_unset_approval()

    # if we finished all components, redirect to '/'
    if component is None:
        return redirect('/')

    # else setup the appropriate component

    if component == 'address':
        return setup_address(request)

    if component == 'jacobs':
        return setup_jacobs(request)

    if component == 'social':
        return setup_social(request)

    if component == 'job':
        return setup_job(request)

    # and redirect to / in the fallback case
    return render(request, 'registry/portal/done.html')


def setup_address(request):
    """ Sets up a setup form for an address. """

    if request.method == 'POST':
        # load the form
        form = AddressForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # Create the Address form
            instance = form.save(commit=False)
            instance.member = request.user.alumni
            instance.save()

            request.user.alumni.approval.save()

            # and then continue to the main portal page.
            return redirect('/setup/')

    # if we did not have any post data, simply create a new form
    else:
        form = AddressForm()

    # and return the request
    return render(request, 'registry/portal/setup.html',
                  {'form': form, 'name': 'Address Information'})


def setup_jacobs(request):
    """ Sets up a bootstrap form for jacobs data. """

    if request.method == 'POST':
        # load the form
        form = JacobsForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # Create the Address form
            instance = form.save(commit=False)
            instance.member = request.user.alumni
            instance.save()

            request.user.alumni.approval.save()

            # and then continue to the main portal page.
            return redirect('/setup/')

    # if we did not have any post data, simply create a new form
    else:
        form = JacobsForm()

    # and return the request
    return render(request, 'registry/portal/setup.html',
                  {'form': form, 'name': 'Jacobs Data'})


def setup_social(request):
    """ Sets up a bootstrap form for social media. """

    if request.method == 'POST':
        # load the form
        form = SocialMediaForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # Create the Address form
            instance = form.save(commit=False)
            instance.member = request.user.alumni
            instance.save()

            request.user.alumni.approval.save()

            # and then continue to the main portal page.
            return redirect('/setup/')

    # if we did not have any post data, simply create a new form
    else:
        form = SocialMediaForm()

    # and return the request
    return render(request, 'registry/portal/setup.html',
                  {'form': form, 'name': 'Social Media'})


def setup_job(request):
    """ Sets up a bootstrap form for job information. """

    if request.method == 'POST':
        # load the form
        form = JobInformationForm(request.POST)

        # check that the form is valid
        if form.is_valid():
            form.clean()

            # Create the Address form
            instance = form.save(commit=False)
            instance.member = request.user.alumni
            instance.save()

            request.user.alumni.approval.save()

            # and then continue to the main portal page.
            return redirect('/setup/')

    # if we did not have any post data, simply create a new form
    else:
        form = JobInformationForm()

    # and return the request
    return render(request, 'registry/portal/setup.html',
                  {'form': form, 'name': 'Job Information'})
