from .models import GoogleAssociation
from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError


from google.oauth2 import id_token
from google.auth.transport import requests


class GoogleTokenBackend():
    def authenticate(self, request, token=None):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GSUITE_OAUTH_CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong token issuer')

            # Verify it's an account from our own domain
            if idinfo['hd'] != settings.GSUITE_DOMAIN_NAME:
                raise ValueError('Wrong hosted domain')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            user_id = idinfo['sub']

            # Find a local user with corresponding Google user ID
            user = GoogleAssociation.objects.get(google_user_id=user_id)

            return user.user

        except (ValueError, GoogleAssociation.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
