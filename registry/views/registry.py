from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
    """ Renders either the home page or the portal. """

    # if the user is signed in, redirect to the main portal
    if request.user.is_authenticated() and request.user.alumni:
        return redirect(reverse('portal'))

    # else render the home page
    return render(request, 'registry/index.html')


@login_required
def portal(request):
    # check if we have anything left to setup
    unset = request.user.alumni.get_first_unset_approval()

    # and redirect there
    if unset is not None:
        return redirect(reverse('setup'))

    # and render the portal
    return render(request, 'portal/index.html', {'user': request.user})
