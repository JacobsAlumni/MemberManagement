from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import views

from django.contrib.auth import authenticate, login

from django.conf import settings
from . import backend

# Create your views here.

# Tries to log a user in using a token supplied by Google.


def google_token_login(request):
    if request.method != 'POST':
        raise SuspiciousOperation('Wrong request method')

    token = request.POST['token']

    res = authenticate(request, token=token)

    if res is not None:
        login(request, res)
        return HttpResponse('OK')
    else:
        return HttpResponseForbidden('NOK')

# Injects the OAuth client ID into the template context


class ClientIdLoginView(views.LoginView):
    extra_context = {
        'client_id': settings.GSUITE_OAUTH_CLIENT_ID,
        'gsuite_domain': settings.GSUITE_DOMAIN_NAME
    }
