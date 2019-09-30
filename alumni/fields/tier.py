from .custom import CustomTextChoiceField

__all__ = ['TierField']


class TierField(CustomTextChoiceField):
    STARTER = 'st'
    CONTRIBUTOR = 'co'
    PATRON = 'pa'

    CHOICES = (
        (CONTRIBUTOR,
         "Contributor (Standard package if graduated more than 2 years ago): 39€ p.a."),
        (STARTER,
         "Starter (If graduated less than 2 years ago or not ready to financially contribute): free"),
        (PATRON,
         "Patron (Premium package for those who want to contribute more): 249€ p.a."),
    )

    DEFAULT_CHOICE = CONTRIBUTOR
