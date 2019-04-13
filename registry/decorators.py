from django.contrib.auth.decorators import user_passes_test

from django.urls import reverse
from django.shortcuts import redirect

from django.http import HttpResponseForbidden

def user_has_alumni(user):
    """ Safely checks if a user has an alumni """
    try:
        user.alumni
        return True
    except:
        return False

def require_alumni(view):
    """ A decorator for views that ensures an alumni exists or raise http forbidden"""

    def wrapper(request, *args, **kwargs):
        if not user_has_alumni(request.user):
            return HttpResponseForbidden('User missing Alumni. Contact Support if this is unexpected. ')
        
        return view(request, *args, **kwargs)
    
    return wrapper


def require_setup_completed(view):
    """ A decorator for views that ensures that and alumni has setup all components """

    @require_alumni
    def wrapper(request, *args, **kwargs):
        # if we are missing a component, return to the main page
        if not request.user.alumni.setup_completed:
            return redirect(reverse('setup'))

        # else use the normal one
        return view(request, *args, **kwargs)

    # and return the wrapper
    return wrapper
