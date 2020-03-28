from __future__ import annotations

from sesame import utils as token_utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.contrib.auth.models import User


def generate_login_token(user: User) -> str:
    """ Generates a login token for a user """

    token_params = token_utils.get_parameters(user)
    return token_params['url_auth_token']
