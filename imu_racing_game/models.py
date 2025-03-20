from django.db import models
from uuid import uuid4


class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class HighScore(UUIDModel):
    class GameType(models.TextChoices):
        RACING = "RACING", "Racing"

    username = models.SlugField(max_length=100, unique=True)
    score = models.PositiveIntegerField()

    game_type = models.CharField(
        choices=GameType.choices,
        max_length=max(len(choice.value) for choice in GameType),
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = ["username", "game_type"]
