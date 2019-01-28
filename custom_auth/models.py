from django.db import models
from django.contrib import auth
# Create your models here.


class GoogleAssociation(models.Model):
    user = models.ForeignKey(auth.get_user_model())
    google_user_id = models.CharField(max_length=64)
