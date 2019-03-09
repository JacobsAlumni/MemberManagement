from django.conf import settings

NEEDS_DEVEL_WARNING = getattr(settings, 'ENABLE_DEVEL_WARNING',
                              False)
IS_STRIPE_TEST_MODE = "_test_" in (getattr(settings, "STRIPE_SECRET_KEY", "_test_") or '__test__')


def devel_warning(request):
    return {'show_devel_warning': NEEDS_DEVEL_WARNING}

def is_stripe_test_mode(request):
    return {'stripe_test_mode': IS_STRIPE_TEST_MODE}

def map_view_allowed(request):
    from atlas.views import can_view_map
    return {'can_view_map': request.user and can_view_map(request.user)}    