from django.db import transaction

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from custom_auth.gsuite import make_directory_service
from custom_auth.models import GoogleAssociation

class Command(BaseCommand):
    help = 'Links Google and Portal Accounts'

    def add_arguments(self, parser):
        parser.add_argument('users', nargs='*', help='Usernames of user(s) to update. If empty, update all users. ')
        parser.add_argument('--remove-password', '-r', action='store_true', dest='remove_password', help='If provided, remove password login for non-staff non-superuser users. ')

    def handle(self, *args, **kwargs):
        # Get the user objects from the database
        usernames = kwargs['users']
        if len(usernames) == 0:
            users = get_user_model().objects.all()
        else:
            users = get_user_model().objects.filter(username__in=usernames)
        
        link_gsuite_users(users, remove, lambda x: print(x))

def link_gsuite_users(users, remove, on_message):
    """ Links GSuite Users """

    # Create a GSuite Service
    service = make_directory_service()

    for user in users.filter(alumni__approval__approval = True):
        with transaction.atomic():
            # Remove their password if requested
            if remove:
                if (not user.is_staff and not user.is_superuser):
                    on_message("Removed password for user {}".format(user.username))
                    user.set_unusable_password()
                    user.save()
                else:
                    on_message("Did not remove password for user {} (is a staff or superuser)".format(user.username))

            
            # And link them
            link = GoogleAssociation.link_user(user, service = service)
            if link is None:
                on_message("Unable to link user {}: Unable to find GSuite (does it exist?)".format(user.username))
            else:
                on_message("Linked user {} to G-Suite ID {}".format(user.username, link.google_user_id))