from django.conf import settings

def google_analytics_id(request):
    return {'google_analytics_id': settings.GOOGLE_ANALYTICS_ID }