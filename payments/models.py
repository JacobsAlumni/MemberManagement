from django.db import models

from django.utils import timezone
from datetime import timedelta

from alumni.models import Alumni
from alumni.fields import TierField

from registry.alumni import AlumniComponentMixin

from payments import stripewrapper


@Alumni.register_component(6)
class MembershipInformation(AlumniComponentMixin, models.Model):
    """ The (payment-related) membership information of an Alumni Member """

    SETUP_COMPONENT_NAME = 'membership'

    member = models.OneToOneField(
        Alumni, related_name='membership', on_delete=models.CASCADE)

    tier = TierField(help_text='Membership Tier')

    customer = models.CharField(max_length=255, null=True, blank=True,
                                help_text='The stripe customer id for the user')


@Alumni.register_component(7)
class SubscriptionInformation(AlumniComponentMixin, models.Model):
    SETUP_COMPONENT_NAME = 'subscription'

    member = models.ForeignKey(
        Alumni, on_delete=models.CASCADE)

    start = models.DateTimeField(
        help_text='The start date for the subscription')
    end = models.DateTimeField(
        blank=True, null=True, help_text='The end date for the subscription')

    subscription = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='The Stripe Subscription ID for the given subscription')
    external = models.BooleanField(default=False, help_text="Subscription is managed externally")

    tier = TierField(help_text='Membership Tier')

    def cancel(self):
        """ Cancels this subscription along with the stripe subscription """
        if self.end is not None:
            raise Exception('Subscription already cancelled')

        if not self.subscription:
            raise Exception('Can not cancel subscription: No subscription')

        # cancel the subscription
        sub, err = stripewrapper.cancel_subscription(self.subscription)
        if err is not None:
            return False

        # and set the end of the subscription
        self.set_end()

        return

    def set_end(self):
        """ Marks this subscription as having ended """
        if not self.active:
            raise Exception('Subscription is already ended')

        # store now as the end of the subscription
        self.end = timezone.now()

    @property
    def active(self):
        """ Property indicating if the subscription is active """

        return self.end is None or (self.end > timezone.now())

    @property
    def time_left(self):
        """ Return the time left until the subscription expires or None """

        # if we are not active or are no longer active
        if not self.active or self.end is None:
            return None

        # return the timedelta left
        return timezone.now() - self.end

    @classmethod
    def create_starter_subscription(cls, alumni):
        # creates a new starter subscription
        return cls.start_new_subscription(alumni, None, length=timedelta(days=2 * 365))

    @classmethod
    def start_new_subscription(cls, alumni, subscription, length=None, tier=None):
        # the new subscription starts now
        start = timezone.now()

        # compute the end of the subscription
        end = None
        if length is not None:
            if not isinstance(length, timedelta):
                raise TypeError(
                    'Expected length to be datetime.timedelta or None')

            end = start + length

        # if there is an old subscription, throw an error
        if alumni.subscription is not None:
            raise ValueError('User already has a subscription')

        # If we did not create an alumni membership, create a new one
        if tier is None:
            tier = alumni.membership.tier

        # and create the new subscription
        return cls.objects.create(member=alumni, start=start, end=end, subscription=subscription, tier=tier)
