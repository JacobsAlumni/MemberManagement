from __future__ import annotations

from django.conf import settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Any
    from django.http import HttpRequest

NEEDS_DEVEL_WARNING = getattr(settings, "ENABLE_DEVEL_WARNING", False)


def devel_warning(request: HttpRequest) -> Dict[str, Any]:
    return {"show_devel_warning": NEEDS_DEVEL_WARNING}
