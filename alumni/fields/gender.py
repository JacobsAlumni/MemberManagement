from __future__ import annotations

from .custom import CustomTextChoiceField

__all__ = ['GenderField']


class GenderField(CustomTextChoiceField):
    FEMALE = 'fe'
    MALE = 'ma'
    OTHER = 'ot'
    UNSPECIFIED = 'un'

    CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (OTHER, 'Non-binary'),
        (UNSPECIFIED, 'Prefer not to say'),
    )

    DEFAULT_CHOICE = UNSPECIFIED
