from django.db import models

__all__ = ['CollegeField']

class CollegeField(models.IntegerField):
    KRUPP = 1
    MERCATOR = 2
    CIII = 3
    NORDMETALL = 4
    CV = 5
    COLLEGE_CHOICES = (
        (KRUPP, 'Krupp'),
        (MERCATOR, 'Mercator'),
        (CIII, 'College III'),
        (NORDMETALL, 'Nordmetall'),
        (CV, 'College V')
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = CollegeField.COLLEGE_CHOICES
        super(CollegeField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CollegeField, self).deconstruct()
        del kwargs['choices']
        return name, path, args, kwargs