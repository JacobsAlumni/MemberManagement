from payments import stripewrapper
from datetime import datetime
import pytz

from django.db import transaction

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from alumni.models import SetupCompleted

class Command(BaseCommand):
    help = 'Updates setup date from Stripe Account Data'

    def add_arguments(self, parser):
        parser.add_argument('users', nargs='*', help='Usernames of user(s) to update. If empty, update all users. ')

    def handle(self, *args, **kwargs):
        # Get the user objects from the database
        usernames = kwargs['users']
        if len(usernames) == 0:
            sss = SetupCompleted.objects.all()
        else:
            sss = SetupCompleted.objects.filter(member__profile__username__in=usernames)
        
        fetch_from_stripe(sss, lambda x: print(x))

def fetch_from_stripe(sss, on_message):
    """ Updates the setup date from stripe """

    for s in sss:
        username = s.member.profile.username
        cid = s.member.membership.customer

        date, e = stripewrapper.safe(lambda stripe: stripe.Customer.retrieve(cid).created)
        if e is not None:
            on_message('Unable to retrieve customer creation date for {}'.format(username))
            continue
        
        s.date = datetime.utcfromtimestamp(date).replace(tzinfo=pytz.utc)
        s.save()

        on_message('Updated {} date to {}'.format(username, s.date))
