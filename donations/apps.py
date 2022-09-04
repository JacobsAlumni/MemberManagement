from django.apps import AppConfig


class DonationsConfig(AppConfig):
    name = 'donations'

    def ready(self) -> None:
        import donations.signals
        return super().ready()