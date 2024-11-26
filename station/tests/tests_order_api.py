from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Order, Journey, TrainType, Train, Route, Station, Ticket
from station.serializers import OrderSerializer, OrderRetrieveSerializer

ORDER_URL = reverse("station:order-list")


def detail_url(order_id):
    return reverse("station:order-detail", args=[order_id])


class JourneyUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_order_list(self):
        user2 = get_user_model().objects.create_user(
            username="volodymyr",
            password="test123",
        )
        Order.objects.create(
            user=self.user,
        )
        Order.objects.create(
            user=user2,
        )
        response = self.client.get(ORDER_URL)
        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_order_detail(self):
        self.source = Station.objects.create(name="Source Station")
        self.destination = Station.objects.create(name="Destination Station")

        self.route = Route.objects.create(
            source=self.source,
            destination=self.destination,
        )

        self.train = Train.objects.create(
            name="Train 1",
            cargo_number=1,
            places_in_cargo=100,
            train_type=TrainType.objects.create(name="Passenger"),
        )

        self.journey = Journey.objects.create(
            train=self.train,
            route=self.route,
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
        )

        order = Order.objects.create(user=self.user)

        self.ticket_1 = Ticket.objects.create(
            train=self.train,
            cargo=1,
            seat=10,
            journey=self.journey,
            order=order,
        )
        self.ticket_2 = Ticket.objects.create(
            train=self.train,
            cargo=1,
            seat=20,
            journey=self.journey,
            order=order,
        )
        url = detail_url(order.id)

        response = self.client.get(url)
        serializer = OrderRetrieveSerializer(order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_create(self):
        self.source = Station.objects.create(name="Source Station")
        self.destination = Station.objects.create(name="Destination Station")

        self.route = Route.objects.create(
            source=self.source,
            destination=self.destination,
        )

        self.train = Train.objects.create(
            name="Train 1",
            cargo_number=1,
            places_in_cargo=100,
            train_type=TrainType.objects.create(name="Passenger"),
        )

        self.journey = Journey.objects.create(
            train=self.train,
            route=self.route,
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
        )

        payload = {
            "tickets": [
                {
                    "train": self.train.id,
                    "cargo": 1,
                    "seat": 10,
                    "journey": self.journey.id,
                },
                {
                    "train": self.train.id,
                    "cargo": 1,
                    "seat": 20,
                    "journey": self.journey.id,
                },
            ]
        }
        response = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 1)
