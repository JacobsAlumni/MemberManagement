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

    tier = TierField(default=TierField.CONTRIBUTOR,
                     help_text='Membership Tier')

    desired_tier = TierField(null=True, blank=True,
                             help_text='Desired Membership Tier')

    customer = models.CharField(max_length=255, null=True, blank=True,
                                help_text='The stripe customer id for the user')

    stripe_check = models.BooleanField(
        null=True, blank=True, help_text='Internal Column used by Stripe checking')

    def create_subscription(self):
        """ Creates a new subscription when newly entered payment details are available """

        # if we have a 'desired_tier' this should be used to create the subscription
        # as there are now payment methods available.
        if self.desired_tier is not None:
            tier = self.desired_tier
            update_mode = True
        else:
            tier = self.tier
            update_mode = False

        # Create a stripe subscription on the given plan

        plan = TierField.get_stripe_id(tier)
        sub_id, err = stripewrapper.create_subscription(self.customer, plan)
        if err is not None:
            return None

        # if we updated the tier
        if update_mode:
            if self.member.subscription is not None:
                self.member.subscription.set_end()
            self.tier = self.desired_tier
            self.desired_tier = None
            self.save()

        # finally create the actual subscription object
        instance = SubscriptionInformation.start_new_subscription(
            self.member, sub_id, length=None, tier=tier)
        if update_mode and instance is not None:
            instance.created_from_update = True
        return instance

    def change_tier(self, desired_tier):
        """ Designates this user as changing tier """

        # if the desired tier is none, we are already done
        if desired_tier is None:
            return self.member.subscription, None

        # we are already on the desired tier
        # so remove the desired_tier flag
        if desired_tier == self.tier:
            self.desired_tier = None
            self.save()
            return self.member.subscription, None

        # There are 3*2 = 6 possiblitlies for switche

        # we close the current subscription and start a new starter one
        # Contributor -> Starter
        # Patron -> Starter
        if desired_tier == TierField.STARTER:
            return self._downgrade_to_starter()

        # we need to ask for payment details because we don't have them yet
        # - Starter -> Contributor
        # - Starter -> Patron
        if self.tier == TierField.STARTER:
            return self._upgrade_to_payed(desired_tier)

        # we switch between payed tiers and pro-rate
        # Contributor -> Patron
        # Patron -> Contributor
        return self._switch_payed_tier(desired_tier)

    def _downgrade_to_starter(self):
        # cancel the active subscription
        sub = self.member.subscription
        if sub is not None:
            if not sub.cancel():
                return None, 'Unable to cancel active subscription'

        # set the tier to starter
        self.tier = TierField.STARTER
        self.desired_tier = None
        self.save()

        # create a new starter subscription
        instance = SubscriptionInformation.create_starter_subscription(
            self.member)

        # remove all the payment sources
        _, err = stripewrapper.clear_all_payment_sources(self.customer)
        if err is not None:
            return None, 'Unable to remove payment methods'

        # and return the instance
        return instance, None

    def _upgrade_to_payed(self, desired_tier):
        """ Upgrades from the free to the desired tier """

        # store the 'desired' tier, so that we know to ask for payment details
        self.desired_tier = desired_tier
        self.save()

        return None, None

    def _switch_payed_tier(self, desired_tier):
        """ Switches the payed tier """

        # find the current subscription
        sub = self.member.subscription
        if sub is None or sub.subscription is None:
            return None, 'Cannot find current subscription'
        subscription = sub.subscription

        # update the remote subscription
        plan = TierField.get_stripe_id(desired_tier)
        _, err = stripewrapper.update_subscription(subscription, plan)
        if err is not None:
            return None, 'Unable to switch subscription to new plan'

        # end the current subscription, set the new tier
        sub.set_end()
        self.tier = desired_tier
        self.save()

        # Create the new subscription
        instance = SubscriptionInformation.start_new_subscription(
            self.member, subscription, tier=desired_tier)
        return instance, None


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
    external = models.BooleanField(
        default=False, help_text="Subscription is managed externally")

    tier = TierField(help_text='Membership Tier')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_from_update = False

    @classmethod
    def component_exists(cls, alumni):
        """ Checks if an alumni has this component set """

        # if we don't have a subscription the component does not exist
        if not SubscriptionInformation.objects.filter(member=alumni).exists():
            return False

        # if we have no membership, we don't have this component
        obj = MembershipInformation.objects.get(member=alumni)
        if obj is None:
            return False

        # if the desired_tier is already done, then we are done
        return obj.desired_tier is None

    def cancel(self):
        """ Cancels this subscription along with the stripe subscription """
        if self.end is not None:
            raise Exception('Subscription already cancelled')

        if not self.subscription:
            raise Exception('Can not cancel subscription: No subscription')

        # cancel the subscription
        _, err = stripewrapper.cancel_subscription(self.subscription)
        if err is not None:
            return False

        # and set the end of the subscription
        self.set_end()

        return True

    def set_end(self):
        """ Marks this subscription as having ended """

        self.end = timezone.now()
        self.save()

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

        # If we did not create an alumni membership, create a new one
        if tier is None:
            tier = alumni.membership.tier

        # and create the new subscription
        return cls.objects.create(member=alumni, start=start, end=end, subscription=subscription, tier=tier)
