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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"cargo: {self.cargo}, seat: {self.seat}"
