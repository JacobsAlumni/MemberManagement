from django.utils import timezone

class AlumniSubscriptionMixin:

    @property
    def subscription(self):
        return self.subscriptioninformation_set.exclude(end__lte=timezone.now()).order_by('start').first()
    
    @property
    def can_update_payment(self):
        """ Checks if the user is allowed to update their payment method """

        sub = self.subscription
        if sub is None:
            return False
        
        stripesub = sub.subscription
        return stripesub is not None and stripesub != ''