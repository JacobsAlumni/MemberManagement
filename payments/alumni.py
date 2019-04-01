from datetime import datetime

class AlumniSubscriptionMixin:

    #@property
    #def payment(self):
    #    import warnings
    #    warnings.warn('Alumni.payment has been renamed to Alumni.membership', DeprecationWarning)
    #    return self.membership

    @property
    def active_subscription(self):
        return self.subscriptioninformation_set.filter(member=self).exclude(end__lte=datetime.now()).order_by('start').first()