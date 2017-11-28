from django import template
from django.template.loader import get_template
from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION >= (1, 10, 0):
    context_class = dict
else:
    # Django<1.10 compatibility
    from django.template import Context

    context_class = Context

register = template.Library()


def _get_widget_class(name):
    if name.startswith('checkbox'):
        return 'uk-checkbox'
    if name.startswith('select') or name.startswith('lazyselectmultiple'):
        return 'uk-select'
    if name.startswith('radio'):
        return 'uk-radio'
    if name.startswith('textarea'):
        return 'uk-textarea'
    return 'uk-input'


def _add_class(widget, cls):
    if cls is not None:
        try:
            widget.attrs["class"] += cls
        except KeyError:
            widget.attrs["class"] = cls + " "


def _preprocess_fields(form):
    for afield, field in zip(form, form.fields):

        # add a class for the input element
        name = form.fields[field].widget.__class__.__name__.lower()
        _add_class(form.fields[field].widget, _get_widget_class(name))

        # add a class for the validation

        if afield.errors:
            _add_class(form.fields[field].widget, 'uk-form-danger')


    return form


@register.filter
def as_uikit_form(form):
    template = get_template("uikit/form.html")
    form = _preprocess_fields(form)

    c = context_class({
        "form": form,
    })
    return template.render(c)


@register.filter
def css_class(field):
    return field.field.widget.__class__.__name__.lower()
