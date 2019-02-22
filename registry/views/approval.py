from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404


from alumni.models import Alumni
from custom_auth.models import GoogleAssociation

from custom_auth.gsuite import get_user_id

EMAIL_OK = 0
EMAIL_DIFFERS = 1
EMAIL_DOESNOTEXIST = 2
EMAIL_LINKEDOTHER = 3

EMAIL_HUMAN = {
    EMAIL_OK: '',
    EMAIL_DIFFERS: 'Differs from assigned address',
    EMAIL_DOESNOTEXIST: 'Does not exist on GSuite',
    EMAIL_LINKEDOTHER: 'Linked to another account'
}

def check_existing_email(alumni):
    """ Checks consistency with the existing email field """

    emailLinked = alumni.profile.googleassociation_set.exists()

    if emailLinked and alumni.existingEmail != alumni.approval.gsuite:
        return EMAIL_DIFFERS
            
    # if we have not linked check if the email exists
    elif not emailLinked and alumni.existingEmail:
        google_user_id = get_user_id(alumni.existingEmail)
        if google_user_id is None:
            return EMAIL_DOESNOTEXIST
        elif GoogleAssociation.objects.filter(google_user_id=google_user_id).exists():
            return EMAIL_LINKEDOTHER

    return EMAIL_OK

class ApprovalView(TemplateView):
    template_name = 'approval/index.html'

    def get_context_data(self, **kwargs):
        alumni = get_object_or_404(Alumni, profile__id=kwargs['id'])

        emailLinked = alumni.profile.googleassociation_set.exists()

        previousEmail = EMAIL_HUMAN[check_existing_email(alumni)]

        return {'alumni': alumni, 'emailLinked': emailLinked, 'previousEmail': previousEmail }
    
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)