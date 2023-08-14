from __future__ import annotations

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.urls import reverse as reverse_func

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse


class RedirectResponseMixin:
    """A mixin that can be used to redirect the user"""

    def redirect_response(
        self, url: str, reverse: bool = True, permanent: bool = False
    ) -> HttpResponse:
        if reverse:
            url = reverse_func(url)

        redirect_class = HttpResponseRedirect
        if permanent:
            redirect_class = HttpResponsePermanentRedirect

        return redirect_class(url)


class UnauthorizedResponseMixin:
    """A mixin that can be used to send an unauthorized response to the user"""

    def unauthorized_response(
        self, text: str = "Unauthorized", code: int = 403
    ) -> HttpResponse:
        return HttpResponse(text, status=code)
