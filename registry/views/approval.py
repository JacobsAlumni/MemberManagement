from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from alumni.models import Alumni



class ApprovalView(TemplateView):
    template_name = 'approval/index.html'

    def get_context_data(self, **kwargs):
        alumni = get_object_or_404(Alumni, profile__id=kwargs['id'])
        return {'alumni': alumni}
    
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)