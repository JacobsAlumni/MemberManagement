def atlas_allowed(request):
    from atlas.views import can_view_atlas
    return {'can_view_atlas': request.user and can_view_atlas(request.user)}