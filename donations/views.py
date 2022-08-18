import stripe
from babel.numbers import get_currency_precision
from django.urls import reverse
from django.utils.translation import gettext
from django.views.generic import CreateView, TemplateView, DetailView

from donations.models import Donation


def money_to_integer(money):
    return int(
        money.amount * (
            10 ** get_currency_precision(money.currency.code)
        )
    )


class DonateView(CreateView):
    model = Donation
    fields = ["amount", "target"]

    def get_success_url(self):
        # Create a Stripe Checkout Session
        session: stripe.checkout.Session = stripe.checkout.Session.create(
            cancel_url=self.request.build_absolute_uri(reverse('donate')),
            success_url=self.request.build_absolute_uri(reverse('donation-detail', args=(str(self.object.external_id),))),
            mode="payment",
            currency=self.object.amount_currency,
            line_items=[
                {
                    "price_data": {
                        "currency": self.object.amount_currency,
                        "product_data": {
                            "name": gettext("Donation")
                        },
                        "unit_amount": money_to_integer(self.object.amount),
                    },
                    "quantity": 1
                }
            ]
        )

        self.object.payment_id = session.payment_intent
        self.object.save()

        return session.url


class DonationSuccessView(DetailView):
    model = Donation
    template_name = "donations/success.html"
    slug_field = "external_id"

class DonationFailedView(TemplateView):
    template_name = "donations/failed.html"
