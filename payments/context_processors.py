from __future__ import annotations

from django.conf import settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.http import HttpRequest
    from typing import Dict, Any


IS_STRIPE_TEST_MODE = "_test_" in (
    getattr(settings, "STRIPE_SECRET_KEY", "_test_") or '__test__')


def stripe(request: HttpRequest) -> Dict[str, Any]:
    return {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_test_mode': IS_STRIPE_TEST_MODE
    }

def tier(request: HttpRequest) -> Dict[str, Any]:
    return {
        'selfservice_tier_enabled': settings.SELFSERVICE_TIER_ENABLED
    }
