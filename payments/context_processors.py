from django.conf import settings

IS_STRIPE_TEST_MODE = "_test_" in (
    getattr(settings, "STRIPE_SECRET_KEY", "_test_") or '__test__')


def stripe(request):
    return {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_test_mode': IS_STRIPE_TEST_MODE
    }
