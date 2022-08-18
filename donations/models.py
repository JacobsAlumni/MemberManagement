from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext
from djmoney.models import fields as money_fields

from alumni import models as alumni_models

# Create your models here.
class DonationTarget(models.Model):
    """These are options a user can choose to donate towards"""
    label = models.CharField(max_length=512)
    active = models.BooleanField(default=True)


class Donation(models.Model):
    """These are created when a user fires a donation. We create a Stripe checkout session and send them there."""

    # This can be used to build a success URL for Stripe Checkout
    external_id = models.UUIDField(default=uuid4)

    # A user can specify what to donate towards - or leave it blank
    target = models.ForeignKey(DonationTarget, verbose_name=gettext("Donating towards"), null=True, blank=True, on_delete=models.SET_NULL)
    amount = money_fields.MoneyField(max_digits=5, decimal_places=2, default_currency='EUR')

    # Anonymous donations get linked to a stripe customer with this
    # This also gives us the anonymous user email
    payment_id = models.CharField(max_length=64)

    # When the donation has been processed successfully, this is set.
    completed = models.BooleanField(default=False)

    # Alumni donations use the existing donation receipt flow, no fields required here


@receiver(signals.post_save, sender='payments.PaymentIntent')
def _maybe_generate_donation_receipt(sender, instance, created, **kwargs):
    data = instance.data

    if data['currency'] != 'eur':
        return

    if data['status'] != 'succeeded':
        try:
            donation = Donation.objects.get(payment_id=data['id'])
            donation.completed = True
            donation.save()
        except Donation.DoesNotExist:
            pass
