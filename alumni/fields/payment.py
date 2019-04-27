from django.db import models

__all__ = ['PaymentTypeField']

class PaymentTypeField(models.CharField):
    CARD = 'card'
    SEPA = 'sepa'

    PAYMENT_CHOICES = (
        (CARD,
         "Credit or Debit Card"),
        (SEPA,
         "Automatic Bank Transfer (SEPA)"),
    )

    def __init__(self, **kwargs):
        kwargs['max_length'] = 4
        kwargs['choices'] = PaymentTypeField.PAYMENT_CHOICES
        kwargs['default'] = PaymentTypeField.CARD
        super(PaymentTypeField, self).__init__(**kwargs)
