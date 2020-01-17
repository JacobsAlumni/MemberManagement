from .custom import CustomTextChoiceField

__all__ = ['TierField']


class TierField(CustomTextChoiceField):
    STARTER = 'st'
    CONTRIBUTOR = 'co'
    PATRON = 'pa'

    CHOICES = (
        (CONTRIBUTOR,
         "Contributor – Standard membership for 39€ p.a."),
        (STARTER,
         "Starter – Free Membership (for those not ready or willing to financially contribute) for 0€ p.a."),
        (PATRON,
         "Patron – Premium membership (incl. additional benefits) for 249€ p.a."),
    )

    DEFAULT_CHOICE = CONTRIBUTOR
