from django.dispatch import receiver
from django.db.models import signals
from channels import layers
from asgiref import sync

from donations.utils import get_total_payments

@receiver(signals.post_save, sender='payments.PaymentIntent')
def _maybe_complete_donation(sender, instance, created, **kwargs):
    # Only notify when a PaymentIntent succeeds
    if instance.data["status"] == "succeeded":
        total_amount = get_total_payments()
        new_amount = instance.data["amount"]

        layer = layers.get_channel_layer()
        sync.async_to_sync(layer.group_send)("donation_updates", {"type": "donations.total", "amounts": {"total": total_amount, "current": new_amount}})
