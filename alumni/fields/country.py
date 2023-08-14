from __future__ import annotations

from django_countries.fields import CountryField as OriginalCountryField
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from django_countries.fields import Country
    from django.db.models.expressions import Expression
    from django.db.backends.base.base import BaseDatabaseWrapper

__all__ = ["CountryField"]


class CountryField(OriginalCountryField):
    """Country Field represents a CountryField"""

    COUNTRY_CHOICES = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value_to_string(self, obj: Country) -> str:
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(
        self, value: Any, expression: Expression, connection: BaseDatabaseWrapper
    ) -> Country:
        return self.get_clean_value(value)

    def to_python(self, value: str) -> Country:
        return self.get_clean_value(value)


CountryField.COUNTRY_CHOICES = CountryField().get_choices(include_blank=False)
