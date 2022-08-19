import stripe
from babel.numbers import get_currency_precision
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import gettext
from django.views.generic import CreateView, TemplateView, DetailView

from donation_receipts.models import STRIPE, DonationReceipt
from donations.models import Donation


def money_to_integer(money):
    return int(
        money.amount * (
            10 ** get_currency_precision(money.currency.code)
        )
    )


def user_to_stripe_customer_id(user):
    try:
        return user.alumni.membership.customer
    except ObjectDoesNotExist:
        pass


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
            customer=user_to_stripe_customer_id(self.request.user),
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        try:
            ctx.update({
                "receipt": DonationReceipt.objects.get(payment_stream=STRIPE, payment_reference=self.object.payment_id)
            })
        except DonationReceipt.DoesNotExist:
            pass

        return ctx

class DonationFailedView(TemplateView):
    template_name = "donations/failed.html"
