from payments import models

def get_total_payments():
    all_succeeded = models.PaymentIntent.objects.filter(data__status="succeeded")
    total_amount = sum(map(lambda x: x.data["amount"], all_succeeded))

    return total_amount
