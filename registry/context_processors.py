from django.conf import settings

NEEDS_DEVEL_WARNING = getattr(settings, 'ENABLE_DEVEL_WARNING',
                              False)

def devel_warning(request):
    return {'show_devel_warning': NEEDS_DEVEL_WARNING}
