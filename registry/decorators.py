from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

def user_has_alumni(user):
    """ Safely checks if a user has an alumni """
    try:
        user.alumni
        return True
    except:
        return False

def require_alumni(view):
    """ A decorator for views that ensures an alumni exists """

    # Check that the user passes the test
    return user_passes_test(user_has_alumni)(view)


def require_unset_component(component, alternative):
    """ A decorator for views that ensures a given alumni property does not exist """

    def decorator(view):
        @require_alumni
        def wrapper(request, *args, **kwargs):
            # if the given component does not exist, go to the alternate view
            if request.user.alumni.has_component(component):
                return alternative(request, *args, **kwargs)

            # else use the normal one
            return view(request, *args, **kwargs)

        # and return the wrapper
        return wrapper

    # and return the decorator
    return decorator


def require_setup_completed(alternative):
    """ A decorator for views that ensures that and alumni has setup all components """

    def decorator(view):
        @require_alumni
        def wrapper(request, *args, **kwargs):
            # if we are missing a component, return to the main page
            if not request.user.alumni.setup_completed:
                return alternative(request, *args, **kwargs)

            # else use the normal one
            return view(request, *args, **kwargs)

        # and return the wrapper
        return wrapper

    # and return the decorator
    return decorator
