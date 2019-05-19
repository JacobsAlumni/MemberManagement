from django.conf import settings
from .mailutils import send_email
import datetime

from alumni import fields

from django.shortcuts import render

class AlumniEmailMixin:
    def __get_email_context(self, password=None, back=False):
        """ Gets the context for a welcome (back) email sent to this user """

        return {
            'FullName': self.fullName,
            'Tier': {
                fields.TierField.PATRON: 'Patron',
                fields.TierField.CONTRIBUTOR: 'Contributor',
                fields.TierField.STARTER: 'Starter'
            }[self.membership.tier],
            'CurrentDate': datetime.date.today().strftime('%d %B %Y'),
            'Email': self.approval.gsuite,
            'Password': password,
        }

    def send_welcome_email(self, password=None, back=False):
        """ Sends a user a Welcome (or welcome back) email """

        context = self.__get_email_context(password=password, back=back)

        # set destination and instantiate email templates
        destination = [email, gsuite] + settings.GSUITE_EMAIL_ALL
        if back:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOMEBACK_SUBJECT, 'emails/approval/existing.html', **context)
        else:
            return send_email(destination, settings.GSUITE_EMAIL_WELCOME_SUBJECT, 'emails/approval/new.html', **context)

    def render_welcome_email(self, request, password=None, back=False):
        """ Previews the welcome (back) email for this user into a request """

        context = self.__get_email_context(password=password, back=back)
        
        # get the right template
        if back:
            template = 'emails/approval/existing.html'
        else:
            template = 'emails/approval/new.html'
        
        # and render it
        return render(request, template, context)