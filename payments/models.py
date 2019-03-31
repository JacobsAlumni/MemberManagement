from django.db import models
from jsonfield import JSONField

from alumni.models import Alumni
from alumni.fields import TierField, PaymentTypeField

from datetime import datetime


@Alumni.register_component(6)
class MembershipInformation(models.Model):
    """ The (payment-related) membership information of an Alumni Member """

    SETUP_COMPONENT_NAME = 'membership'

    member = models.OneToOneField(
        Alumni, related_name='payment', on_delete=models.CASCADE)

    tier = TierField(help_text='Membership Tier')

    starterReason = models.TextField(null=True, blank=True,
                                     help_text="")
    customer = models.CharField(max_length=255, null=True, blank=True,
                                help_text='The stripe customer id for the user')

@Alumni.register_component(7)
class SubscriptionInformation(models.Model):
    SETUP_COMPONENT_NAME = 'subscription'

    member = models.ForeignKey(
        Alumni, on_delete=models.CASCADE)

    start = models.DateTimeField(
        help_text='The start date for the subscription')
    end = models.DateTimeField(
        blank=True, null=True, help_text='The end date for the subscription')

    subscription = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='The Stripe Subscription ID for the given subscription')

    tier = TierField(help_text='Membership Tier')

    def active(self):
        """ Checks if a subscription is active """

        return self.end is None or (self.end > datetime.now())
    
    @classmethod
    def create_starter_subscription(cls, alumni):
        return cls.objects.create(member = alumni, start = datetime.now(), subscription = None, tier = 'st')

    
    @classmethod
    def active_subscriptions(cls):
        """ Gets the list of all active subscriptions """
        # TODO: This assumes there is at most one active subscription per member
        # but this might not be the case
        return cls.objects.exclude(end__lte=datetime.now())
        
        