from .custom import CustomIntegerChoiceField

__all__ = ['CollegeField']

class CollegeField(CustomIntegerChoiceField):
    KRUPP = 1
    MERCATOR = 2
    CIII = 3
    NORDMETALL = 4
    CV = 5

    CHOICES = (
        (KRUPP, 'Krupp'),
        (MERCATOR, 'Mercator'),
        (CIII, 'College III'),
        (NORDMETALL, 'Nordmetall'),
        (CV, 'College V')
    )
