from django.db import transaction
from rest_framework import serializers

from station.models import (
    Train,
    TrainType,
    Station,
    Route,
    Crew,
    Journey,
    Ticket,
    Order
)


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_number",
            "places_in_cargo",
            "train_type",
        )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name",)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude",)


class RouteSerializer(serializers.ModelSerializer):
    distance = serializers.ReadOnlyField()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time",)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user",)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "train", "cargo", "seat", "journey", "order",)


class TicketListSerializer(TicketSerializer):
    train = serializers.SlugRelatedField(
        read_only=True,
        many=False,
        slug_field="name"
    )


class TicketDetailSerializer(TicketSerializer):
    train = TrainSerializer(many=False)
    journey = JourneySerializer()
    order = OrderSerializer(many=False)
