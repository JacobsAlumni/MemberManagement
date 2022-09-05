from django.dispatch import receiver
from django.db.models import signals
from channels import layers
from asgiref import sync
from donations.models import Donation

from donations.utils import get_total_payments

@receiver(signals.post_save, sender='payments.PaymentIntent')
def _maybe_complete_donation(sender, instance, created, **kwargs):
    # Only notify when a PaymentIntent succeeds
    if instance.data["status"] == "succeeded":
        total_amount = get_total_payments()
        new_amount = instance.data["amount"]
        for_target = None

        # Find donation for this PaymentIntent
        try:
            d = Donation.objects.get(payment_id=instance.data["id"])
            if d.target:
                for_target = str(d.target)
        except Donation.DoesNotExist:
            pass

        layer = layers.get_channel_layer()
        sync.async_to_sync(layer.group_send)("donation_updates", {"type": "donations.total", "amounts": {"total": total_amount, "current": new_amount, "for_target": for_target}})
