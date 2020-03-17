from __future__ import annotations

from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from registry.models import Announcement

from ..decorators import require_setup_completed

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Dict

@method_decorator(require_setup_completed, name='dispatch')
class PortalView(TemplateView):
    template_name = 'portal/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        alumni = self.request.user.alumni
        context.update({
            'user': self.request.user,
            'announcements': Announcement.objects.filter(active=True),
        })

        return context
