from django.conf import settings
from .mailutils import send_email
import datetime

from alumni import fields


class AlumniEmailMixin:
    def send_welcome_email(self, password=None, back=False):
        """ Sends a user a Welcome (or welcome back) email """

        context = {
            'FullName': self.fullName,
            'Tier': {
                fields.TierField.PATRON: 'Patron',
                fields.TierField.CONTRIBUTOR: 'Contributor',
                fields.TierField.STARTER: 'Starter'
            }[self.membership.tier],
            'CurrentDate': datetime.date.today().strftime('%d %B %Y'),
            'Email': self.email,
            'Password': password,
        }

        # set destination and instantiate email templates
        destination = [email, gsuite] + settings.GSUITE_EMAIL_ALL
        if back:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOMEBACK_SUBJECT, 'emails/approval/existing.html', **context)
        else:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOME_SUBJECT, 'emails/approval/new.html', **context)
