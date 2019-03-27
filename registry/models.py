from django.db import models

# Create your models here.

class Announcement(models.Model):
    active = models.BooleanField(help_text="Show Announcement")
    title = models.TextField(help_text="Title (Text)")
    content = models.TextField(help_text="Content (HTML)")

    def __str__(self):
        return "Announcement {}{}".format(repr(self.title), "" if self.active else " (Inactive)")
