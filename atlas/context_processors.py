from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict
    from django.http import HttpRequest

def atlas_allowed(request: HttpRequest) -> Dict[str, bool]:
    from atlas.views import can_view_atlas
    return {'can_view_atlas': request.user and can_view_atlas(request.user)}
