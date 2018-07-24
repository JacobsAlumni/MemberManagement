from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from registry.decorators import require_setup_completed
from registry.models import Announcement


def home(request):
    """ Renders either the home page or the portal. """

    # if the user is signed in, redirect to the main portal
    if request.user.is_authenticated() and request.user.alumni:
        return redirect(reverse('portal'))

    # else render the home page
    return render(request, 'registry/index.html')


@require_setup_completed(lambda request: redirect(reverse('setup')))
def portal(request):

    # and render the portal
    return render(request, 'portal/index.html', {'user': request.user, 'announcements': Announcement.objects.filter(active=True)})


def default_alternative(request):
    """ A view representing the default redirect representation"""

    return redirect(reverse('portal'))
