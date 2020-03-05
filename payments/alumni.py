from django.conf import settings

from alumni.fields import TierField


class AlumniSubscriptionMixin:

    @property
    def subscription(self):
        """ Gets the active subscription of the user """
        subscriptions = self.subscriptioninformation_set
        tier = self.membership.tier

        # for the starter tier, return the latest starter tier
        if tier == TierField.STARTER:
            return subscriptions.filter(tier=TierField.STARTER).order_by('-start').first()

        # for other tiers, return the open tiers
        return subscriptions.filter(tier=tier, end__isnull=True).order_by('-start').first()

    @property
    def can_update_payment(self):
        """ Checks if the user is allowed to update their payment method """

        sub = self.subscription
        if sub is None:
            return False

        stripesub = sub.subscription
        return stripesub is not None and stripesub != ''

    @property
    def can_update_tier(self):
        """ Checks if the user can change their tier """
        return self.setup_completed and settings.SELFSERVICE_TIER_ENABLED
