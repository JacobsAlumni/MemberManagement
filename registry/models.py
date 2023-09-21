from __future__ import annotations

from alumni.models import Alumni

from django.db import models
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Optional


class VoteLink(models.Model):
    active: bool = models.BooleanField(
        help_text="Enable showing this vote link", default=False
    )

    title: str = models.TextField(help_text="Title of this link")
    description: str = models.TextField(help_text="Description of this link")

    url: str = models.URLField(
        help_text="URL where the vote takes place. Use ${token} as a placeholder for the token. "
    )

    def get_token(self, alumni: Alumni) -> VoteToken:
        obj, _ = VoteToken.objects.get_or_create(vote=self, alumni=alumni)
        return obj

    @property
    def tokens(self) -> Iterable[VoteLink]:
        return VoteToken.objects.filter(vote=self)

    def __str__(self) -> str:
        return "Vote Link {} to {}".format(self.title, self.url)


class VoteToken(models.Model):
    class Meta:
        ordering = ("token",)
        unique_together = (("vote", "alumni"),)

    @property
    def triple(self) -> [str, bool, str]:
        """Returns a triple (url, is_personalized, token)"""
        url = self.vote.url
        is_personalized = "${token}" in url
        token = self.token
        url = url.replace("${token}", str(token))
        return url, is_personalized, token

    vote: VoteLink = models.ForeignKey(
        VoteLink, on_delete=models.CASCADE, help_text="Vote this Token is associated to"
    )
    alumni: Alumni = models.ForeignKey(
        Alumni, on_delete=models.CASCADE, help_text="Alumni this token is for"
    )
    token: str = models.UUIDField(default=uuid.uuid4, unique=True)


class Announcement(models.Model):
    active: bool = models.BooleanField(help_text="Show Announcement")
    title: str = models.TextField(help_text="Title (Text)")
    content: str = models.TextField(help_text="Content (HTML)")

    def __str__(self):
        return "Announcement {}{}".format(
            repr(self.title), "" if self.active else " (Inactive)"
        )
