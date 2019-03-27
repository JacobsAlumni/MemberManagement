from django.conf import settings

IS_STRIPE_TEST_MODE = "_test_" in (getattr(settings, "STRIPE_SECRET_KEY", "_test_") or '__test__')

def is_stripe_test_mode(request):
    return {'stripe_test_mode': IS_STRIPE_TEST_MODE}
