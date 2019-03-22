from django.db import models
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist

from custom_auth.gsuite import make_directory_service, get_user_id

class GoogleAssociation(models.Model):
    user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    google_user_id = models.CharField(max_length=64)

    @classmethod
    def link_user(cls, user, service = None):
        # Get the approval object
        try:
            approval = user.alumni.approval
        # or return that it does not exist
        except ObjectDoesNotExist as e:
            return None
        
        # If there is no gsuite email we can not link
        if approval.gsuite is None:
            return None
        
        # get the user id
        google_user_id = get_user_id(approval.gsuite, service = service)
        
        # or return None if we do not have one
        if google_user_id is None:
            return None

        # Create or update the object
        obj, created = cls.objects.update_or_create(user=user, defaults={'google_user_id': google_user_id})

        # if the user is not staff and is not a superuser
        # then we need to lock their password 
        if not (user.is_staff or user.is_superuser):
            user.set_unusable_password()
            user.save()
        
        # and return the object itself for convenience
        return obj