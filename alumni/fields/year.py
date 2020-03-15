from __future__ import annotations

from .custom import CustomIntegerChoiceField

__all__ = ['ClassField']


class ClassField(CustomIntegerChoiceField):
    OTHER = 0000
    C_2004 = 2004
    C_2005 = 2005
    C_2006 = 2006
    C_2007 = 2007
    C_2008 = 2008
    C_2009 = 2009
    C_2010 = 2010
    C_2011 = 2011
    C_2012 = 2012
    C_2013 = 2013
    C_2014 = 2014
    C_2015 = 2015
    C_2016 = 2016
    C_2017 = 2017
    C_2018 = 2018
    C_2019 = 2019
    C_2020 = 2020
    C_2021 = 2021
    C_2022 = 2022
    C_2023 = 2023
    C_2024 = 2024
    C_2025 = 2025
    CHOICES = (
        (OTHER, 'Other (Please specify in comments)'),
        (C_2004, 'Class of 2004'),
        (C_2005, 'Class of 2005'),
        (C_2006, 'Class of 2006'),
        (C_2007, 'Class of 2007'),
        (C_2008, 'Class of 2008'),
        (C_2009, 'Class of 2009'),
        (C_2010, 'Class of 2010'),
        (C_2011, 'Class of 2011'),
        (C_2012, 'Class of 2012'),
        (C_2013, 'Class of 2013'),
        (C_2014, 'Class of 2014'),
        (C_2015, 'Class of 2015'),
        (C_2016, 'Class of 2016'),
        (C_2017, 'Class of 2017'),
        (C_2018, 'Class of 2018'),
        (C_2019, 'Class of 2019'),
        (C_2020, 'Class of 2020'),
        (C_2021, 'Class of 2021'),
        (C_2022, 'Class of 2022'),
        (C_2023, 'Class of 2023'),
        (C_2024, 'Class of 2024'),
        (C_2025, 'Class of 2025'),
    )

    DEFAULT_CHOICE = OTHER
