from __future__ import annotations

import unicodedata
from django.contrib.auth.models import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional


def generate_username(first_names: str, middle_names: Optional[str], family_name: str) -> str:
    """ Given a full name, generates a unique username """

    # assemble the full name
    full_name = first_names + " " + \
        (middle_names if middle_names is not None else "") + " " + family_name

    # normalize unicode chars
    # adapted from https://djangosnippets.org/snippets/723/
    name = unicodedata.normalize('NFKD', full_name.lower()).encode('ASCII', 'ignore')

    # use only characters
    chars = []
    for character in name.decode('utf8'):
        if character.isalpha() or character == ' ':
            chars.append(character)
    name = ''.join(chars).split()

    # use the first letter of the given name, and then entire family name
    base_username = '{}{}'.format(name[0][0], name[-1])

    # first candidate
    username = base_username
    if User.objects.filter(username=username).exists():
        # keep adding a number to the username, until a nonexistent one is found
        number = 1
        username = base_username + str(number)
        while User.objects.filter(username=username).exists():
            number = number + 1
            username = base_username + str(number)

    return username
