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
         "Starter – Free Membership for 0€ p.a."),
        (PATRON,
         "Patron – Premium membership for 249€ p.a."),
    )

    STRIPE_IDS = {
        CONTRIBUTOR: "contributor-membership",
        STARTER: "starter-membership",
        PATRON: "patron-membership"
    }

    @staticmethod
    def get_description(value):
        for (k, v) in TierField.CHOICES:
            if k == value:
                return v

    @staticmethod
    def get_stripe_id(value):
        return TierField.STRIPE_IDS[value]
