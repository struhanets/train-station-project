from django.db import models

from TrainStation.settings import AUTH_USER_MODEL
from user.models import User


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_number = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey("TrainType", on_delete=models.CASCADE, related_name="trains")

    class Meta:
        verbose_name_plural = "trains"
        ordering = ("name",)

    @property
    def seats_in_train(self):
        return self.cargo_number * self.places_in_cargo

    def __str__(self):
        return f"{self.name}"


class TrainType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "stations"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="routes")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE)
    distance = models.FloatField(null=True, blank=True)

    @property
    def title(self):
        # Формуємо динамічне поле title на основі значень source, destination та distance
        return f"{self.source.name} - {self.destination.name}, distance: {self.distance}"

    def __str__(self):
        # Використовуємо властивість title для представлення об'єкта як рядка
        return self.title


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ("last_name",)

    def __str__(self):
        return f"name: {self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.departure_time} on train {self.train.name}, route {self.route}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user} buy a ticket for {self.created_at}"


class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_tickets")
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="journey_tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("seat", "journey")
        ordering = ("seat",)

    def __str__(self):
        return f"{self.journey} - (seat - {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_rise):
        if not (1 <= seat <= num_seats):
            raise error_to_rise(
                {
                    "seat": f"The seat must be in range [1, {num_seats}]"
                }
            )
