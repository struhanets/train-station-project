# Generated by Django 5.1.3 on 2024-11-14 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("station", "0011_alter_ticket_journey_alter_ticket_train"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ("seat",)},
        ),
    ]