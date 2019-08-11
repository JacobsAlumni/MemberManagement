from .custom import CustomTextChoiceField

__all__ = ['AlumniCategoryField']


class AlumniCategoryField(CustomTextChoiceField):
    REGULAR = 're'
    FACULTY = 'fa'
    FRIEND = 'fr'

    CHOICES = (
        (REGULAR, 'Alumni (Former Student)'),
        (FACULTY, 'Faculty or Staff'),
        (FRIEND, 'Friend Of The Association')
    )

    DEFAULT_CHOICE = REGULAR
