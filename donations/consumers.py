from channels.generic.websocket import JsonWebsocketConsumer

import donations.utils


class DonationUpdateConsumer(JsonWebsocketConsumer):
    groups = ["donation_updates"]

    def connect(self):
        ret = super().connect()
        self.send_json({"type": "donations.total", "amounts": {"total": donations.utils.get_total_payments()}})

    def donations_total(self, event):
        self.send_json(event)
