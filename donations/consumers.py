from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from donations.utils import get_total_payments

class DonationUpdateConsumer(JsonWebsocketConsumer):
    groups = ["donation_updates"]

    def connect(self):
        ret = super().connect()
        self.send_json({"type": "donations.total", "amounts": {"total": get_total_payments()}})

    def donations_total(self, event):
        self.send_json(event)
