import datetime
from uuid import uuid4

import stripe
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext
from djmoney.models import fields as money_fields

from MemberManagement import mailutils
from alumni import models as alumni_models


class DonationTarget(models.Model):
    """These are options a user can choose to donate towards"""
    label = models.CharField(max_length=512)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.label


class Donation(models.Model):
    """These are created when a user fires a donation. We create a Stripe checkout session and send them there."""

    # This can be used to build a success URL for Stripe Checkout
    external_id = models.UUIDField(default=uuid4)

    # A user can specify what to donate towards - or leave it blank
    target = models.ForeignKey(DonationTarget, verbose_name=gettext("Donating towards"), null=True, blank=True, on_delete=models.SET_NULL)
    amount = money_fields.MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')

    # Anonymous donations get linked to a stripe customer with this
    # This also gives us the anonymous user email
    payment_id = models.CharField(max_length=64)

    # When the donation has been processed successfully, this is set.
    completed = models.DateTimeField(null=True, blank=True)

    # Alumni donations use the existing donation receipt flow, no fields required here


@receiver(signals.post_save, sender='payments.PaymentIntent')
def _maybe_complete_donation(sender, instance, created, **kwargs):
    data = instance.data

    if data['currency'] != 'eur':
        return

    if data['status'] == 'succeeded':
        try:
            donation = Donation.objects.get(payment_id=data['id'])
            donation.completed = datetime.datetime.now()
            donation.save()
        except Donation.DoesNotExist:
            pass

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(signals.post_save, sender='payments.PaymentIntent')
def _maybe_complete_donation(sender, instance, created, **kwargs):
    all_succeeded = sender.objects.filter(data__status="succeeded")
    total_amount = sum(map(lambda x: x.data["amount"], all_succeeded))

    layer = get_channel_layer()
    async_to_sync(layer.group_send)("donation_updates", {"type": "donations.total", "total_amount": total_amount})



@receiver(signals.post_save, sender='donations.Donation')
def _maybe_email_donor(sender, instance: Donation, created, **kwargs):
    if not instance.completed:
        return

    pi: stripe.PaymentIntent = stripe.PaymentIntent.retrieve(instance.payment_id)
    receipt_email = pi.receipt_email

    domain = Site.objects.get_current().domain

    mail = mailutils.prepare_email(receipt_email, 'Jacobs Alumni Association - Thank You!',
                                   'emails/donation_complete.html', object=instance, domain=domain)

    mail.send()
