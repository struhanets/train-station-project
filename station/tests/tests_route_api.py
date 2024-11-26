from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Station, Route
from station.serializers import RouteListSerializer

ROUTE_URL = reverse('station:route-list')


def route_sample(**params):
    default_source = Station.objects.create(name='default_source')
    default_destination = Station.objects.create(name='default_destination')
    defaults = {
        "source": default_source,
        "destination": default_destination
    }

    defaults.update(params)
    return Route.objects.create(**defaults)


class RouteUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TrainAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test", password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_trains_list(self):
        route_sample()

        response = self.client.get(ROUTE_URL)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_routes_filter_by_source(self):
        route = route_sample()

        response = self.client.get(ROUTE_URL, {"source": f"{route.source.name}"})
        serializer = RouteListSerializer([route], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_routes_filter_by_destination(self):
        route = route_sample()

        response = self.client.get(ROUTE_URL, {"destination": f"{route.destination.name}"})
        serializer = RouteListSerializer([route], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_routes_create(self):
        default_source = Station.objects.create(name='default_source')
        default_destination = Station.objects.create(name='default_destination')

        payload = {
            "source": default_source.id,
            "destination": default_destination.id,
        }

        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        route = Route.objects.get(id=response.data["id"])
        for key in payload.keys():
            if key == "source":
                self.assertEqual(payload[key], route.source.id)
            elif key == "destination":
                self.assertEqual(payload[key], route.destination.id)
            else:
                self.assertEqual(payload[key], getattr(route, key))
