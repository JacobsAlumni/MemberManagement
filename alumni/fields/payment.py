from .custom import CustomTextChoiceField

__all__ = ['PaymentTypeField']


class PaymentTypeField(CustomTextChoiceField):
    CARD = 'card'
    SEPA = 'sepa'

    CHOICES = (
        (CARD,
         "Credit or Debit Card"),
        (SEPA,
         "Automatic Bank Transfer (SEPA)"),
    )
