# Generated by Django 5.1.3 on 2024-11-11 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("station", "0008_ticket_unique_ticket_seat_journey"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="ticket",
            name="unique_ticket_seat_journey",
        ),
    ]
