from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse as reverse_func

class RedirectResponseMixin:
    """ A mixin that can be used to redirect the user """

    def redirect_response(self, url, reverse = False, permanent = False):
        if reverse:
            url = reverse_func(url)
        
        redirect_class = HttpResponseRedirect
        if permanent:
            redirect_class = HttpResponsePermanentRedirect

        return redirect_class(url)

class UnauthorizedResponseMixin:
    """ A mixin that can be used to send an unauthorized response to the user """

    def unauthorized_response(self, text = 'Unauthorized', code = 403):
        return HttpResponse(text, status=code)
