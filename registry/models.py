from django.db import models

# Create your models here.


class SubscriptionPlan(object):
    def __init__(self, name, stripe_id, cost, currency):
        self.name = name
        self.stripe_id = stripe_id
        self.cost = cost

# The subscription values are in Euro-Cents :)
subscription_plans = {
    "st": SubscriptionPlan("Starter Subscription", "starter-subscription", 100, "EUR"),
    "co": SubscriptionPlan("Contributor Subscription", "contributor-subscription", 4900, "EUR"),
    "pa": SubscriptionPlan("Patron Subscription", "patron-subscription", 24900, "EUR"),
}