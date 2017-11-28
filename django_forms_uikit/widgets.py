# -*- coding: utf-8 -*-
from json import dumps as json_dumps

from django.forms.widgets import DateInput


class DatePickerInput(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'uikit/field_date.html'