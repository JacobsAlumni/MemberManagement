from __future__ import annotations

from .custom import CustomTextChoiceField

__all__ = ["DegreeField"]


class DegreeField(CustomTextChoiceField):
    FOUNDATION_YEAR = "fy"
    BACHELOR_ARTS = "ba"
    BACHELOR_SCIENCE = "bsc"
    MASTER_ARTS = "ma"
    MASTER_SCIENCE = "msc"
    PHD = "phd"
    MBA = "mba"

    CHOICES = (
        (FOUNDATION_YEAR, "Foundation Year"),
        (BACHELOR_ARTS, "Bachelor of Arts"),
        (BACHELOR_SCIENCE, "Bachelor of Science"),
        (MASTER_ARTS, "Master of Arts"),
        (MASTER_SCIENCE, "Master of Science"),
        (PHD, "PhD"),
        (MBA, "MBA"),
    )
