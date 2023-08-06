import typing
from payments import models

from djmoney.contrib.exchange.models import convert_money
from moneyed import Money


def make_money(x: models.PaymentIntent):
    return Money(x.data["amount"], x.data["currency"])


def get_total_payments():
    all_succeeded = models.PaymentIntent.objects.filter(data__status="succeeded")

    totals = {}
    for pi in all_succeeded:
        totals[pi.data["currency"]] = (
            totals.get(pi.data["currency"], 0) + pi.data["amount"]
        )
    return totals
