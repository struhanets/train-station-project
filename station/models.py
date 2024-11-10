import math

from django.db import models
from django.db.models import UniqueConstraint

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

    def __str__(self):
        return f"{self.name}, type of-{self.train_type} with {self.cargo_number} cargos"


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

    def save(self, *args, **kwargs):
        # Перевіряємо, чи є у станцій координати
        if (
            self.source.latitude
            and self.source.longitude
            and self.destination.latitude
            and self.destination.longitude
        ):
            self.distance = self.calculate_distance(
                self.source.latitude, self.source.longitude,
                self.destination.latitude, self.destination.longitude
            )
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Радіус Землі в кілометрах
        R = 6371.0

        # Перетворення широти та довготи з градусів у радіани
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Різниця координат
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Формула Гарвіна
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Відстань
        distance = R * c
        return round(distance, 2)

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}, distance: {self.distance} km."


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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)


class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="tickets")
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seat", "journey"], name="unique_ticket_seat_journey")
        ]
