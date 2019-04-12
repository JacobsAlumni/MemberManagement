from django.core.management.base import BaseCommand

from payments import stripewrapper
from payments.models import SubscriptionInformation

from alumni.fields import TierField

from datetime import timedelta




class Command(BaseCommand):
    help = 'Removes legacy data from Stripe'

    def add_arguments(self, parser):
        parser.add_argument('users', nargs='*', help='Usernames of user(s) to update. If empty, update all users. ')
    def handle(self, *args, **kwargs):
        # Get the user objects from the database
        usernames = kwargs['users']
        if len(usernames) == 0:
            subs = SubscriptionInformation.objects.all()
        else:
            subs = SubscriptionInformation.objects.filter(member__profile__username__in=usernames)
        
        subs = subs.filter(tier=TierField.STARTER).exclude(subscription__isnull=True).exclude(subscription='')
        
        clear_legacy_data(subs, lambda x: print(x))

def clear_legacy_data(subs, on_message):
    """ Links GSuite Users """

    subs = subs.select_related('member__membership')
    for s in subs:
        subscription = s.subscription
        customer = s.member.membership.customer

        _, err = stripewrapper.cancel_subscription(subscription)
        if err is not None:
            on_message("Did not cancel subscription from {}: {}".format(customer, err))
            continue
        else:
            on_message("Cleared subscription from {}".format(customer))

        # clear out the subscription
        s.subscription = None
        s.end = s.start + timedelta(days = 2 * 365)
        s.save()

    # Remove payment sources of all the members
    cids = subs.values('member__membership__customer').distinct()
    for c in cids:
        customer = c['member__membership__customer']
        _, err = stripewrapper.clear_all_payment_sources(customer)
        if err is not None:
            on_message("Did not remove payment sources from {}: {}".format(customer, err))
        else:
            on_message("Removed payment sources from {}".format(customer))