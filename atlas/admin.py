from django.contrib import admin

from .models import GeoLocation

# Register your models here.

class GeoAdmin(admin.ModelAdmin):
    list_filter = ('country', )
    list_display = ('country', 'zip', 'lat', 'lon')
    search_fields = ('country', 'zip')

admin.site.register(GeoLocation, GeoAdmin)