from uuid import uuid4
from django.db import models
from djmoney import money
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
    target = models.ForeignKey(DonationTarget, null=True, blank=True, on_delete=models.SET_NULL)
    amount = money.Money()

    # Anonymous donations get linked to a stripe customer with this
    # This also gives us the anonymous user email
    checkout_session_id = models.CharField(max_length=64)

    # When the donation has been processed successfully, this is set.
    completed = models.BooleanField()

    # Alumni donations use the existing donation receipt flow, no fields required here