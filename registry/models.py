from django.db import models

# Create your models here.


class SubscriptionPlan(object):
    def __init__(self, name, stripe_id, cost, currency):
        self.name = name
        self.stripe_id = stripe_id
        self.cost = cost
        self.currency = currency

# The subscription values are in Euro-Cents :)
subscription_plans = {
    "st": SubscriptionPlan("Starter Membership", "starter-membership", 100, "EUR"),
    "co": SubscriptionPlan("Contributor Membership", "contributor-membership", 4900, "EUR"),
    "pa": SubscriptionPlan("Patron Membership", "patron-membership", 24900, "EUR"),
}