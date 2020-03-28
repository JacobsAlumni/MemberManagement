from __future__ import annotations

from django.conf import settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, Any
    from django.http import HttpRequest



def google_analytics_id(request: HttpRequest) -> Dict[str, Any]:
    return {'google_analytics_id': settings.GOOGLE_ANALYTICS_ID}

def js_testmode_flag(request: HttpRequest) -> Dict[str, Any]:
    return {'js_test_mode_flag': settings.JS_TEST_MODE_FLAG }
