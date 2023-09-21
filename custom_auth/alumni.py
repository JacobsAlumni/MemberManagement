from __future__ import annotations

import datetime

from django.conf import settings
from django.shortcuts import render

from alumni import fields

from MemberManagement.mailutils import send_email

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Any
    from django.http import HttpRequest, HttpResponse


class AlumniEmailMixin:
    def __get_email_context(
        self, password: Optional[str] = None, back: bool = False
    ) -> Dict[str, Any]:
        """Gets the context for a welcome (back) email sent to this user"""

        return {
            "FullName": self.fullName,
            "Tier": {
                fields.TierField.PATRON: "Patron",
                fields.TierField.CONTRIBUTOR: "Contributor",
                fields.TierField.STARTER: "Starter",
            }[self.membership.tier],
            "CurrentDate": datetime.date.today().strftime("%d %B %Y"),
            "Email": self.approval.gsuite,
            "Password": password,
        }

    def send_welcome_email(
        self, password: Optional[str] = None, back: bool = False
    ) -> int:
        """Sends a user a Welcome (or welcome back) email"""

        context = self.__get_email_context(password=password, back=back)

        # extract email and gsuite address
        email = self.email
        gsuite = self.approval.gsuite

        # set destination and instantiate email templates
        destination = [email, gsuite] + settings.GSUITE_EMAIL_ALL
        if back:
            return send_email(
                destination,
                settings.GSUITE_EMAIL_WELCOMEBACK_SUBJECT,
                "emails/approval/existing.html",
                **context,
            )
        else:
            return send_email(
                destination,
                settings.GSUITE_EMAIL_WELCOME_SUBJECT,
                "emails/approval/new.html",
                **context,
            )

    def render_welcome_email(
        self, request: HttpRequest, password: Optional[str] = None, back: bool = False
    ) -> HttpResponse:
        """Previews the welcome (back) email for this user into a request"""

        context = self.__get_email_context(password=password, back=back)

        # get the right template
        if back:
            template = "emails/approval/existing.html"
        else:
            template = "emails/approval/new.html"

        # and render it
        return render(request, template, context)
