from __future__ import annotations
from django.utils.decorators import method_decorator
import json

from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.forms import Form
    from django.http import HttpRequest, HttpResponse

from ..forms import RegistrationForm


@method_decorator(csrf_protect, name='dispatch')
class FormValidationView(View):
    """ A view that can be posted with form data to validate it """

    # the form this view is validating
    form: Form = None

    @classmethod
    def instantiate_form(cls, request: HttpRequest) -> Form:
        """ Used to instantiate the form given a request"""
        return cls.form(request.POST)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ Validates form data via POST """

        # instatiate the form
        form = self.__class__.instantiate_form(request)
        
        # check if the form is valid
        valid = form.is_valid()
        errors = json.loads(form.errors.as_json())

        # and return the response
        return JsonResponse(data={"valid": valid, "errors": errors})


class RegistrationValidationView(FormValidationView):
    form = RegistrationForm
