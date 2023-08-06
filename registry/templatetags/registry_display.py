from __future__ import annotations

from django import template

register = template.Library()

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


@register.filter("get_choice_field")
def get_choice_field(instance: Any, name: str) -> Any:
    try:
        choices = dict(type(instance)._meta.get_field(name).choices)
        value = getattr(instance, name)
        if isinstance(value, list):
            return [choices[v] for v in value]
        else:
            return choices[value]
    except:
        return ""


@register.filter("print_boolean")
def print_boolean(value: bool) -> str:
    return "Yes" if value else "No"
