import math

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
    Order,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = (
            "id",
            "name",
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
            "seats_in_train",
        )


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = (
            "id",
            "name",
            "latitude",
            "longitude",
        )


class RouteSerializer(serializers.ModelSerializer):
    distance = serializers.ReadOnlyField()

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
            "title",
        )

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Формула Гарвіна для обчислення відстані між двома координатами"""
        R = 6371.0  # Радіус Землі в кілометрах
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance, 2)  # Округлення до 2 знаків після коми

    def create(self, validated_data):
        # Обчислюємо distance, якщо координати вказані
        source = validated_data["source"]
        destination = validated_data["destination"]
        if (
            source.latitude
            and source.longitude
            and destination.latitude
            and destination.longitude
        ):
            validated_data["distance"] = self.calculate_distance(
                source.latitude,
                source.longitude,
                destination.latitude,
                destination.longitude,
            )
        return super().create(validated_data)


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "train",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "train",
            "cargo",
            "seat",
            "journey",
        )

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"], attrs["train"].seats_in_train, serializers.ValidationError
        )
        return attrs


class JourneyRetrieveSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(read_only=True, slug_field="title")
    train = TrainSerializer()
    taken_seats = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="seat", source="journey_tickets"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "train",
            "taken_seats",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class TicketListSerializer(TicketSerializer):
    train = TrainSerializer(many=False, read_only=True)
    journey = JourneySerializer(many=False, read_only=True)


class OrderRetrieveSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
