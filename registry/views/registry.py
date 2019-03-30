from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from registry.decorators import require_setup_completed
from registry.models import Announcement

@require_setup_completed(lambda request: redirect(reverse('setup')))
def portal(request):
    # and render the portal
    return render(request, 'portal/index.html', {'user': request.user, 'announcements': Announcement.objects.filter(active=True)})


def default_alternative(request):
    """ A view representing the default redirect representation"""

    return redirect(reverse('portal'))
