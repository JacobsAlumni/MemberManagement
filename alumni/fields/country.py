from django_countries.fields import CountryField as OriginalCountryField

__all__ = ['CountryField']


class CountryField(OriginalCountryField):
    """ Country Field represents a CountryField """

    COUNTRY_CHOICES = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        return self.get_clean_value(value)

    def to_python(self, value):
        return self.get_clean_value(value)


CountryField.COUNTRY_CHOICES = CountryField().get_choices(include_blank=False)
