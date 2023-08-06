from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils import dateparse

from payments import stripewrapper
from payments.models import MembershipInformation, PaymentIntent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable, Callable
    from argparse import ArgumentParser


class Command(BaseCommand):
    help = "Pulls all PaymentIntents from the Stripe API"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "since",
            nargs="?",
            default=None,
            help="If specified, only pulls PaymentIntents created after that date.",
        )

    @staticmethod
    def _sync_payment_intent(pi_instance):
        pi_db, created = PaymentIntent.objects.update_or_create(
            stripe_id=pi_instance["id"], defaults={"data": pi_instance}
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        since = dateparse.parse_date(kwargs["since"])
        print(stripewrapper.map_payment_intents(self._sync_payment_intent, since=since))
