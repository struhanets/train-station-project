# Generated by Django 5.1.3 on 2024-11-24 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Crew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("last_name",),
            },
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("distance", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("latitude", models.FloatField(null=True)),
                ("longitude", models.FloatField(null=True)),
            ],
            options={
                "verbose_name_plural": "stations",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("cargo_number", models.IntegerField()),
                ("places_in_cargo", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "trains",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="TrainType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="Journey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
                (
                    "route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="station.route"
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="station.train"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="station.station"
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="routes",
                to="station.station",
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trains",
                to="station.traintype",
            ),
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cargo", models.IntegerField()),
                ("seat", models.IntegerField()),
                (
                    "journey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="journey_tickets",
                        to="station.journey",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="station.order",
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="train_tickets",
                        to="station.train",
                    ),
                ),
            ],
            options={
                "ordering": ("seat",),
                "unique_together": {("seat", "journey")},
            },
        ),
    ]
