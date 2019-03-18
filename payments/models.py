from django.db import models
from jsonfield import JSONField

from alumni.models import Alumni
from alumni.fields import TierField, PaymentTypeField

@Alumni.register_component(6)
class PaymentInformation(models.Model):
    """ The payment information of an Alumni Member """

    member = models.OneToOneField(Alumni, related_name='payment', on_delete=models.CASCADE)

    tier = TierField(help_text='Membership Tier')

    payment_type = PaymentTypeField()

    starterReason = models.TextField(null=True, blank=True,
        help_text="")

    token = models.CharField(max_length=255, null=True, blank=True,
                             help_text='The stripe card token for the user')
    customer = models.CharField(max_length=255, null=True, blank=True,
                                help_text='The stripe customer id for the user')
    subscription = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='The payment token for the customer')
    sepa_mandate = JSONField(blank=True, null=True)
