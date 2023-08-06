from __future__ import annotations

from django.core.exceptions import ObjectDoesNotExist

import csv
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404

from ..models import VoteLink, Announcement

from ..decorators import require_setup_completed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict


@method_decorator(require_setup_completed, name="dispatch")
class VoteLinkView(TemplateView):
    template_name = "portal/vote.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        alumni = self.request.user.alumni

        links = []
        try:
            if alumni.approval.approval:
                links = VoteLink.objects.filter(active=True)
                links = [self.link_to_context(link) for link in links]
        except ObjectDoesNotExist:
            pass

        context.update(
            {
                "user": self.request.user,
                "announcements": Announcement.objects.filter(active=True),
                "links": links,
            }
        )

        return context

    def link_to_context(self, link: VoteLink) -> Dict[str, Any]:
        token = link.get_token(self.request.user.alumni)
        url, is_personalized, token = token.triple
        return {
            "link": link,
            "url": url,
            "is_personalized": is_personalized,
            "token": token,
        }


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class TokenExportView(View):
    def get(self, *args, **kwargs) -> HttpResponse:

        # get the object we are linking
        link = get_object_or_404(VoteLink, pk=kwargs["id"])

        # make a response
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="tokens.csv"'

        # write out all the token
        writer = csv.writer(response)
        for token in link.tokens:
            writer.writerow([token.token])

        return response
