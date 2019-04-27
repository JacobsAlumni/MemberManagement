from django.db import models

__all__ = ['GenderField']

class GenderField(models.CharField):
    FEMALE = 'fe'
    MALE = 'ma'
    OTHER = 'ot'
    UNSPECIFIED = 'un'
    SEX_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (OTHER, 'Non-binary'),
        (UNSPECIFIED, 'Prefer not to say'),
    )

    def __init__(self, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = GenderField.SEX_CHOICES
        kwargs['default'] = GenderField.UNSPECIFIED
        super(GenderField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(GenderField, self).deconstruct()
        del kwargs["max_length"]
        del kwargs['choices']
        del kwargs['default']
        return name, path, args, kwargs