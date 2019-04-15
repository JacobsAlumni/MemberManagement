from django.conf import settings
from .mailutils import send_email

from alumni import fields


class AlumniEmailMixin:
    def send_welcome_email(self, password=None, back=False):
        """ Sends a user a Welcome (or welcome back) email """

        # Extract all the fields from the alumni
        email = self.email
        gsuite = self.approval.gsuite
        name = self.fullName
        tier = {
            fields.TierField.PATRON: 'Patron',
            fields.TierField.CONTRIBUTOR: 'Contributor',
            fields.TierField.STARTER: 'Starter'
        }[self.membership.tier]

        # set destination and instantiate email templates
        destination = [email, gsuite] + settings.GSUITE_EMAIL_ALL
        if back or password is None:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOMEBACK_SUBJECT, 'emails/welcomeback_email.html', name=name, tier=tier, gsuite=gsuite, password=password)
        else:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOME_SUBJECT, 'emails/welcome_email.html', name=name, tier=tier, gsuite=gsuite, password=password)
