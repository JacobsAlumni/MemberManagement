from django.db import models

# Create your models here.

class Announcement(models.Model):
    active = models.BooleanField(help_text="Show Announcement")
    title = models.TextField(help_text="Title (Text)")
    content = models.TextField(help_text="Content (HTML)")

    def __str__(self):
        return "Announcement {}{}".format(repr(self.title), "" if self.active else " (Inactive)")

class SubscriptionPlan(object):
    def __init__(self, name, stripe_id, cost, currency, description):
        self.name = name
        self.stripe_id = stripe_id
        self.cost = cost
        self.currency = currency
        self.description = description

# The subscription values are in Euro-Cents :)
subscription_plans = {
    "st": SubscriptionPlan("Starter Membership", "starter-membership", 100, "EUR", "Recently graduated alumni can get a starter membership for upto 2 years"),
    "co": SubscriptionPlan("Contributor Membership", "contributor-membership", 4900, "EUR", "Contributor membership is for our regular alumni members"),
    "pa": SubscriptionPlan("Patron Membership", "patron-membership", 24900, "EUR", "Patron membership gets you a brick with your name on it on the IUB rocks path"),
}
