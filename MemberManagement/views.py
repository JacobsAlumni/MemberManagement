from django.views.generic.base import View, TemplateResponseMixin
from django.core.exceptions import ObjectDoesNotExist

from MemberManagement.mixins import RedirectResponseMixin, UnauthorizedResponseMixin


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
