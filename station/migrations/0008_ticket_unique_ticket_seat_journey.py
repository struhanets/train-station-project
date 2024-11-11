# Generated by Django 5.1.3 on 2024-11-11 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("station", "0007_remove_ticket_unique_ticket_seat_journey"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("seat", "journey"), name="unique_ticket_seat_journey"
            ),
        ),
    ]
