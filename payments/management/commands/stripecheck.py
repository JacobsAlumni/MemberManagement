from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from payments import stripewrapper
from payments.models import MembershipInformation

from tqdm import tqdm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class Command(BaseCommand):
    help = "Checks Stripe Customer Data"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        try:
            with transaction.atomic():  # Inner atomic block, create a savepoint
                self.handle_check()
                raise IntendedException()  # Raising an exception - abort the savepoint
        except IntendedException:
            pass

    def handle_check(self) -> None:
        # we didn't check anything
        MembershipInformation.objects.update(stripe_check=False)

        # check all the customers
        with tqdm(total=MembershipInformation.objects.count()) as tbar:
            _, err = stripewrapper.map_customers(
                lambda customer: self.check_customer(tbar, customer)
            )
            if err is not None:
                raise err

        # raise an error for non-existent customers
        for info in MembershipInformation.objects.filter(stripe_check=False):
            user = info.member.profile.username
            print(
                "Customer {0!r} (for user {1!r}): Customer not found in Stripe Customer database".format(
                    info.customer, user
                )
            )

    def check_customer(self, tbar: tqdm, stripe_customer: Dict[str, Any]) -> str:
        tbar.update(1)  # next customer seen
        customer_id = stripe_customer["id"]

        # grab the customer in the db
        try:
            info = MembershipInformation.objects.get(customer=customer_id)
        except MembershipInformation.DoesNotExist:
            tbar.write(
                "Customer {0!r}: Customer does not belong to any known Alumni".format(
                    customer_id
                )
            )
            return

        # we used it in the stripe check
        info.stripe_check = True
        info.save()

        errors = stripewrapper.check_customer_stripe_props(info.member, stripe_customer)
        for err in errors:
            tbar.write(err)


class IntendedException(Exception):
    pass
