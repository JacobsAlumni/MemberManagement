from __future__ import annotations

from django.contrib import admin

# Register your models here.
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('active', 'title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('active',)


admin.site.register(Announcement, AnnouncementAdmin)
