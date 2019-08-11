# -*- coding: utf-8 -*-
from json import dumps as json_dumps

from django.forms.widgets import DateInput


class DatePickerInput(DateInput):
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'uikit/field_date.html'

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs, format="%Y-%m-%d")
