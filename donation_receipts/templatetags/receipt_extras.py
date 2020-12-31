from django.template import Library
from donation_receipts import utils

register = Library()


@register.filter
def written(value):
    return utils._convert_to_written(value)


@register.filter
def numeral(value):
    return utils._convert_to_numeral(value)
