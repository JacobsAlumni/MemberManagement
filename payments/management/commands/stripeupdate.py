from __future__ import annotations

from django.core.management.base import BaseCommand

from payments import stripewrapper
from payments.models import MembershipInformation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable, Callable
    from argparse import ArgumentParser


class Command(BaseCommand):
    help = "Updates Stripe Customer Data"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "users",
            nargs="*",
            help="Usernames of user(s) to update. If empty, update all users. ",
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        # Get the user objects from the database
        usernames = kwargs["users"]
        if len(usernames) == 0:
            members = MembershipInformation.objects.all()
        else:
            members = MembershipInformation.objects.filter(
                member__profile__username__in=usernames
            )

        update_stripe_members(members, lambda x: print(x))


def update_stripe_members(
    members: Iterable[MembershipInformation], on_message: Callable[[str], None]
) -> None:
    """Updates all stripe members"""

    for member in members:
        _, error = stripewrapper.update_customer(member.customer, member.member)
        if error is None:
            on_message("Updated {}".format(member.customer))
        else:
            on_message("Failed to update {}: {}".format(member.customer, error))
