from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class DonationUpdateConsumer(JsonWebsocketConsumer):
    groups = ["donation_updates"]

    def donations_total(self, event):
        self.send_json(event)
