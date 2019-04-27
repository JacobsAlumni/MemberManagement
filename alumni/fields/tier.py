from django.db import models

__all__ = ['TierField']

class TierField(models.CharField):
    STARTER = 'st'
    CONTRIBUTOR = 'co'
    PATRON = 'pa'

    TIER_CHOICES = (
        (CONTRIBUTOR,
         "Contributor (Standard package if graduated more than 2 years ago): 39€ p.a."),
        (STARTER,
         "Starter (If graduated less than 2 years ago or not ready to financially contribute): free"),
        (PATRON,
         "Patron (Premium package for those who want to contribute more): 249€ p.a. "),
    )

    TIER_ADMIN_CHOICES = (
        (CONTRIBUTOR,
         "Contributor"),
        (STARTER,
         "Starter"),
        (PATRON,
         "Patron"),
    )

    def __init__(self, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = TierField.TIER_CHOICES
        kwargs['default'] = TierField.CONTRIBUTOR
        super(TierField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TierField, self).deconstruct()
        del kwargs['max_length']
        del kwargs['choices']
        del kwargs['default']
        return name, path, args, kwargs