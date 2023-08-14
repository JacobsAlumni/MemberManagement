from __future__ import annotations

from payments import stripewrapper

from django.core.management.base import BaseCommand

from alumni.models import SetupCompleted

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable, Callable
    from argparse import ArgumentParser


class Command(BaseCommand):
    help = "Updates setup date from Stripe Account Data"

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
            sss = SetupCompleted.objects.all()
        else:
            sss = SetupCompleted.objects.filter(member__profile__username__in=usernames)

        fetch_from_stripe(sss, lambda x: print(x))


def fetch_from_stripe(sss: Iterable[SetupCompleted], on_message: Callable[[str], None]):
    """Updates the setup date from stripe"""

    for s in sss:
        username = s.member.profile.username
        cid = s.member.membership.customer

        date, e = stripewrapper.get_customer_created(cid)
        if e is not None:
            on_message(
                "Unable to retrieve customer creation date for {}".format(username)
            )
            continue

        s.date = date
        s.save()

        on_message("Updated {} date to {}".format(username, s.date))
