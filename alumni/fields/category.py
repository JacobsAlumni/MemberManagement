from django.db import models

__all__ = ['AlumniCategoryField']

class AlumniCategoryField(models.CharField):
    REGULAR = 're'
    FACULTY = 'fa'
    FRIEND = 'fr'
    CATEGORY_CHOICES = (
        (REGULAR, 'Alumni (Former Student)'),
        (FACULTY, 'Faculty or Staff'),
        (FRIEND, 'Friend Of The Association')
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = AlumniCategoryField.CATEGORY_CHOICES
        kwargs['default'] = AlumniCategoryField.REGULAR
        super(AlumniCategoryField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AlumniCategoryField,
                                         self).deconstruct()
        del kwargs["max_length"]
        del kwargs['choices']
        del kwargs['default']
        return name, path, args, kwargs
