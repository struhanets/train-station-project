from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Station
from station.serializers import StationSerializer

STATION_URL = reverse('station:station-list')


def sample_station(**params):
    default = {"name": "Test Station"}

    default.update(params)
    return Station.objects.create(**default)


class TrainUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(STATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TrainAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test", password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_trains_list(self):
        sample_station()

        response = self.client.get(STATION_URL)
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_station_type_create(self):
        payload = {"name": "Test Station"}

        response = self.client.post(STATION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        station = Station.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(station, key))