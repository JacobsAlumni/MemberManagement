from __future__ import annotations

from django.forms.widgets import DateInput

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, Any


class DatePickerInput(DateInput):
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'uikit/field_date.html'

    def __init__(self, attrs: Dict[str, Any]=None):
        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs, format="%Y-%m-%d")
