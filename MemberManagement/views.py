from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin, View

from MemberManagement.mixins import (RedirectResponseMixin,
                                     UnauthorizedResponseMixin)


class HomeView(UnauthorizedResponseMixin, RedirectResponseMixin, TemplateResponseMixin, View):
    template_name = 'static/index.html'

    def get(self, *args, **kwargs):

        try:
            # if the user is signed in, redirect to the main portal
            if self.request.user.is_authenticated and self.request.user.alumni:
                return self.redirect_response('portal', reverse=True)
        except ObjectDoesNotExist:
            return self.unauthorized_response('Unauthorized (no alumni for user)', code=401)

        return self.render_to_response({})

class HealthCheckDynamic(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ok')

class HealthCheckStatic(RedirectResponseMixin, View):
    def get(self, *args, **kwargs):
        return self.redirect_response(static('health.txt'), reverse=False)
