from django import template

register = template.Library()


@register.filter('get_choice_field')
def get_choice_field(instance, name):
    choices = dict(type(instance)._meta.get_field(name).choices)
    value = getattr(instance, name)
    if isinstance(value, list):
        return [choices[v] for v in value]
    else:
        return choices[value]


@register.filter('print_boolean')
def print_boolean(value):
    return 'Yes' if value else 'No'
