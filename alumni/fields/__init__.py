from __future__ import annotations

from .college import CollegeField
from .category import AlumniCategoryField
from .country import CountryField
from .degree import DegreeField
from .job import JobField
from .gender import GenderField
from .industry import IndustryField
from .major import MajorField
from .tier import TierField
from .payment import PaymentTypeField
from .year import ClassField

__all__ = [
    "AlumniCategoryField",
    "ClassField",
    "CollegeField",
    "CountryField",
    "DegreeField",
    "GenderField",
    "IndustryField",
    "JobField",
    "MajorField",
    "TierField",
    "PaymentTypeField",
]
