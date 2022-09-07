import stripe
from babel.numbers import get_currency_precision
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext
from django.forms import ModelForm
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

import donation_receipts.models
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
    except (ObjectDoesNotExist, AttributeError):
        pass


class DonateView(CreateView):
    model = Donation
    fields = ["amount", "target"]

    def get_success_url(self):
        # Create a Stripe Checkout Session
        session: stripe.checkout.Session = stripe.checkout.Session.create(
            customer=user_to_stripe_customer_id(self.request.user),
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
            ],
            cancel_url=self.request.build_absolute_uri(reverse('donate')),
            success_url=self.request.build_absolute_uri(
                reverse('donation-detail', args=(str(self.object.external_id),))),
            payment_method_options={
                "card": {
                    "setup_future_usage": "off_session"
                }
            },
            submit_type="donate",
        )

        self.object.payment_id = session.payment_intent
        self.object.save()

        return session.url


class ReceiptForm(ModelForm):
    class Meta:
        model = donation_receipts.models.DonationReceipt
        fields = ['email_name', 'sender_info']

        labels = {
            "email_name": "Full Name",
            "sender_info": "Name and Address"
        }
        help_texts = {
            "email_name": "As you'd like to be addressed",
            "sender_info": "Your full legal name and your address, on multiple lines"
        }

class ReceiptCreateView(UpdateView):
    form_class = ReceiptForm

    def render_to_response(self, context, **response_kwargs):
        if self.object.finalized:
            return redirect(self.get_success_url())

        return super().render_to_response(context, **response_kwargs)

    def get_object(self, queryset=None):
        donation = Donation.objects.get(external_id=self.kwargs['slug'])
        pi: stripe.PaymentIntent = stripe.PaymentIntent.retrieve(donation.payment_id)

        # get the existing object or created a new one
        obj, created = DonationReceipt.objects.get_or_create(payment_stream=STRIPE, payment_reference=pi.id,
                                                             defaults={'received_on': donation.completed,
                                                                       'amount': donation.amount,
                                                                       'email_to': pi.receipt_email})

        return obj

    def get_success_url(self):
        return reverse('donation-detail', args=(self.kwargs['slug'],))


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
