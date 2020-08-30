from __future__ import annotations

from django.contrib import admin

# Register your models here.
from .models import Announcement, VoteLink

class VoteLinkAdmin(admin.ModelAdmin):
    list_display = ('active', 'title', 'description', 'url')
    search_fields = ('title', 'description', 'url')
    list_filter = ('active', )
admin.site.register(VoteLink, VoteLinkAdmin)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('active', 'title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('active',)

admin.site.register(Announcement, AnnouncementAdmin)
