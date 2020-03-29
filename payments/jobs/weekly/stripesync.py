from __future__ import annotations

from django_extensions.management.jobs import WeeklyJob
from django.core import management

class Job(WeeklyJob):
    help = "Update stripe users"

    def execute(self) -> None:
        return management.call_command("stripeupdate")
