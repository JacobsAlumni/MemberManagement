from __future__ import annotations

from .custom import CustomTextChoiceField

__all__ = ["AlumniCategoryField"]


class AlumniCategoryField(CustomTextChoiceField):
    REGULAR = "re"
    FACULTY = "fa"
    FRIEND = "fr"

    CHOICES = (
        (REGULAR, "Alum (Former Student)"),
        (FACULTY, "Faculty Or Staff"),
        (FRIEND, "Friend Of The Association"),
    )

    DEFAULT_CHOICE = REGULAR
