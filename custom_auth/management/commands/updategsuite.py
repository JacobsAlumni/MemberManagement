from __future__ import annotations

from django.db import transaction

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from custom_auth.utils.gsuite import make_directory_service, patch_user
from custom_auth.models import GoogleAssociation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from django.contrib.auth.models import User
    from django.db.models import QuerySet
    from argparse import ArgumentParser


class Command(BaseCommand):
    help = 'Links Google and Portal Accounts'

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            'users', nargs='*', help='Usernames of user(s) to update. If empty, update all users. ')

    def handle(self, *args, **kwargs) -> None:
        # Get the user objects from the database
        usernames = kwargs['users']
        if len(usernames) == 0:
            users = get_user_model().objects.all()
        else:
            users = get_user_model().objects.filter(username__in=usernames)

        update_gsuite_users(users, lambda x: print(x))


def update_gsuite_users(users: QuerySet, on_message: Callable[str, None]) -> None:
    """ Links GSuite Users """

    # Create a GSuite Service
    service = make_directory_service()

    for user in users.filter(alumni__approval__approval=True):
        gsuite = user.alumni.approval.gsuite
        if gsuite is None:
            continue

        # reset all the password data
        on_message("Updating {} ...".format(gsuite))
        patch_user(user.alumni, email=gsuite, password=None, service=service)
