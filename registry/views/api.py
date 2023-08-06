from __future__ import annotations
from ..forms import RegistrationForm
from django.utils.decorators import method_decorator
import json

from django.forms import ChoiceField
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.forms import Form
    from django.http import HttpRequest, HttpResponse


@method_decorator(csrf_protect, name="dispatch")
class FormValidationView(View):
    """A view that can be posted with form data to validate it"""

    # the form this view is validating
    form: Form = None

    @classmethod
    def instantiate_form(cls, request: HttpRequest) -> Form:
        """Used to instantiate the form given a request"""
        return cls.form(request.POST)

    @classmethod
    def validate_form_tojson(cls, form: Form) -> Dict[str, Any]:
        """Turns a form instance into json representing validated json"""

        valid = form.is_valid()
        # form values
        values = {field.name: field.data for field in form}

        # form errors
        errors = json.loads(form.errors.as_json())

        # form choices
        choices = {
            field.name: field.field.choices if hasattr(field.field, "choices") else None
            for field in form
        }

        return {"valid": valid, "values": values, "choices": choices, "errors": errors}

    def post(self, request: HttpRequest) -> HttpResponse:
        """Validates form data via POST"""
        form = self.__class__.instantiate_form(request)
        return JsonResponse(self.__class__.validate_form_tojson(form))


class RegistrationValidationView(FormValidationView):
    form = RegistrationForm
