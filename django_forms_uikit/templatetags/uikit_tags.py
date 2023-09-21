from __future__ import annotations

from django import template
from django.template.loader import get_template

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.forms import Form, Field
    from django.forms.widgets import Widget


register = template.Library()


def _get_widget_class(name: str) -> str:
    """Gets the name of a widget"""

    if name.startswith("checkbox"):
        return "uk-checkbox"
    if name.startswith("select") or name.startswith("lazyselectmultiple"):
        return "uk-select"
    if name.startswith("radio"):
        return "uk-radio"
    if name.startswith("textarea"):
        return "uk-textarea"
    return "uk-input"


def _add_class(widget: Widget, cls: str) -> None:
    if cls is not None:
        try:
            widget.attrs["class"] += cls
        except KeyError:
            widget.attrs["class"] = cls + " "


def _preprocess_fields(form: Form) -> Form:
    """Preprocess fields"""

    for afield, field in zip(form, form.fields):
        # add a class for the input element
        name = form.fields[field].widget.__class__.__name__.lower()
        _add_class(form.fields[field].widget, _get_widget_class(name))

        # add a class for the validation

        if afield.errors:
            _add_class(form.fields[field].widget, "uk-form-danger")

    return form


@register.filter
def as_uikit_form(form: Form) -> str:
    """Renders a form using UIKit"""
    template = get_template("uikit/form.html")
    form = _preprocess_fields(form)
    return template.render(
        {
            "form": form,
        }
    )


@register.filter
def css_class(field: Field) -> str:
    """The CSS class of a widget"""
    return field.field.widget.__class__.__name__.lower()
