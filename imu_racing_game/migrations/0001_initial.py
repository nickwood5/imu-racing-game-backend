# Generated by Django 5.1.7 on 2025-03-20 03:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HighScore",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("username", models.SlugField(max_length=100, unique=True)),
                ("score", models.PositiveIntegerField()),
                (
                    "game_type",
                    models.CharField(choices=[("RACING", "Racing")], max_length=6),
                ),
            ],
            options={
                "unique_together": {("username", "game_type")},
            },
        ),
    ]
