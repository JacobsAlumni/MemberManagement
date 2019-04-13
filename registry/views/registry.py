from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateResponseMixin

from registry.models import Announcement

from MemberManagement.mixins import RedirectResponseMixin, UnauthorizedResponseMixin

from ..decorators import require_alumni

@method_decorator(require_alumni, name='dispatch')
class PortalView(UnauthorizedResponseMixin, RedirectResponseMixin, TemplateResponseMixin, View):
    template_name = 'portal/index.html'
    def get(self, *args, **kwargs):
        # if we have setup completed, show the announcements
        alumni = self.request.user.alumni
        if alumni.setup_completed:
            return self.render_to_response({
                'user': self.request.user,
                'announcements': Announcement.objects.filter(active=True),
            })
        
        return self.redirect_response('setup', reverse=True)


def default_alternative(request):
    """ A view representing the default redirect representation"""

    return redirect(reverse('portal'))
