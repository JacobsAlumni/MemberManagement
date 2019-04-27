from django.db import models

__all__ = ['DegreeField']

class DegreeField(models.CharField):
    FOUNDATION_YEAR = 'fy'
    BACHELOR_ARTS = 'ba'
    BACHELOR_SCIENCE = 'bsc'
    MASTER_ARTS = 'ma'
    MASTER_SCIENCE = 'msc'
    PHD = 'phd'
    MBA = 'mba'

    DEGREE_CHOICES = (
        (FOUNDATION_YEAR, 'Foundation Year'),
        (BACHELOR_ARTS, 'Bachelor of Arts'),
        (BACHELOR_SCIENCE, 'Bachelor of Science'),
        (MASTER_ARTS, 'Master of Arts'),
        (MASTER_SCIENCE, 'Master of Science'),
        (PHD, 'PhD'),
        (MBA, 'MBA'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 3
        kwargs['choices'] = DegreeField.DEGREE_CHOICES
        super(DegreeField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DegreeField, self).deconstruct()
        del kwargs["max_length"]
        del kwargs['choices']
        return name, path, args, kwargs