from google.oauth2 import service_account
import googleapiclient.discovery

from django.core.management.base import BaseCommand

from custom_auth.models import GoogleAssociation
from alumni.models import Approval

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

class Command(BaseCommand):
    help = 'Links Google Accounts to Portal Accounts'

    def add_arguments(self, parser):
        parser.add_argument('credentialspath', type=str, help='Path to credentials file')
        parser.add_argument('adminusername', type=str, help='Admin username to use for requests')

    def handle(self, *args, **kwargs):
        # setup credentials and delegate to specific user
        credentials = service_account.Credentials.from_service_account_file(kwargs['credentialspath'], scopes=SCOPES)
        delegated_credentials = credentials.with_subject(kwargs['adminusername'])

        # build a service using these credentials
        service = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)

        # Find all the users that have been approved
        for approval in Approval.objects.filter(approval=True):
            profile = approval.member.profile
            email = approval.gsuite

            # Check if their google association exists
            if not self.has_association(profile.username):
                gid = self.get_user_id(service, email)
                print("got {}".format(gid))

                if gid is not None:
                    print("Linking Portal Account for {} to G-Suite ID {}. ".format(email, gid))
                    self.associate(profile, gid)

    def get_user_id(self, service, username):
        """ Gets the GSuite User ID of a user """
        try:
            result = service.users().get(userKey=username, projection='basic').execute()
        except googleapiclient.errors.HttpError:
            return None
        
        return result['id']

    def has_association(self, username):
        """ Checks if a user with the given username has an association to a GSuite Account """
        return GoogleAssociation.objects.filter(user__username=username).count() > 0

    def associate(self, profile, gid):
        """ Links a given profile to a userid """
        
        instance = GoogleAssociation.objects.create(user=profile, google_user_id=gid)
        instance.save()