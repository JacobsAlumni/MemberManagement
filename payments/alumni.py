from __future__ import annotations

from django.conf import settings

from alumni.fields import TierField

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from .models import SubscriptionInformation


class AlumniSubscriptionMixin:

    @property
    def subscription(self) -> Optional[SubscriptionInformation]:
        """ Gets the active subscription of the user """
        subscriptions = self.subscriptioninformation_set
        tier = self.membership.tier

        # for the starter tier, return the latest starter tier
        if tier == TierField.STARTER:
            return subscriptions.filter(tier=TierField.STARTER).order_by('-start').first()

        # for other tiers, return the open tiers
        return subscriptions.filter(tier=tier, end__isnull=True).order_by('-start').first()

    @property
    def can_update_payment(self) -> bool:
        """ Checks if the user is allowed to update their payment method """

        sub = self.subscription
        if sub is None:
            return False

        stripesub = sub.subscription
        return stripesub is not None and stripesub != ''

    @property
    def can_extend_starter(self) -> bool:
        """ Checks if the subscription can be renewed starter """
        sub = self.subscription
        if sub is None:
            return False

        # DEBUG HACK HACK HACK
        return self.subscription.tier == 'st'

        #return sub.can_extend_starter
    
    @property
    def starter_has_expired(self) -> bool:
        """ Checks if the subscription can be renewed starter """
        sub = self.subscription
        if sub is None:
            return False
        # DEBUG HACK HACK HACK
        return self.subscription.tier == 'st'

        return self.subscription.starter_has_expired
        