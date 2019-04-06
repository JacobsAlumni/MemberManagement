from django.utils import timezone

class AlumniSubscriptionMixin:

    @property
    def subscription(self):
        return self.subscriptioninformation_set.exclude(end__lte=timezone.now()).order_by('start').first()