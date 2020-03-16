from __future__ import annotations

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin, View

from MemberManagement.mixins import (RedirectResponseMixin,
                                     UnauthorizedResponseMixin)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from django.http import HttpResponse


class HomeView(UnauthorizedResponseMixin, RedirectResponseMixin, TemplateResponseMixin, View):
    template_name = 'static/index.html'

    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:

        try:
            # if the user is signed in, redirect to the main portal
            if self.request.user.is_authenticated and self.request.user.alumni:
                return self.redirect_response('portal', reverse=True)
        except ObjectDoesNotExist:
            return self.unauthorized_response('Unauthorized (no alumni for user)', code=401)

        return self.render_to_response({})


class HealthCheckDynamic(View):
    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('ok')


class HealthCheckStatic(RedirectResponseMixin, View):
    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return self.redirect_response(static('health.txt'), reverse=False)
