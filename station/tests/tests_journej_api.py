from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Station, TrainType, Journey, Route, Train
from station.serializers import JourneySerializer, JourneyRetrieveSerializer

JOURNEY_URL = reverse("station:journey-list")


def detail_url(journey_id):
    return reverse("station:journey-detail", args=[journey_id])


def journey_sample(**params):
    default_source = Station.objects.create(name="default_source")
    default_destination = Station.objects.create(name="default_destination")
    default_route = Route.objects.create(
        source=default_source,
        destination=default_destination,
    )

    default_train_type = TrainType.objects.create(name="Default")
    default_train = Train.objects.create(
        name="IC000",
        cargo_number=6,
        places_in_cargo=60,
        train_type=default_train_type,
    )
    default_journey = {
        "route": default_route,
        "train": default_train,
        "departure_time": datetime.now(),
        "arrival_time": datetime.now(),
    }
    default_journey.update(params)
    return Journey.objects.create(**default_journey)


class JourneyUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(JOURNEY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class JourneyAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_journeys_list(self):
        journey_sample()
        response = self.client.get(JOURNEY_URL)
        journeys = Journey.objects.all()
        serializer = JourneySerializer(journeys, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["results"], serializer.data)

    def test_journeys_detail(self):
        journey = journey_sample()
        url = detail_url(journey.id)

        response = self.client.get(url)
        serializer = JourneyRetrieveSerializer(journey)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_journeys_create(self):
        default_source = Station.objects.create(name="default_source")
        default_destination = Station.objects.create(name="default_destination")
        default_route = Route.objects.create(
            source=default_source,
            destination=default_destination,
        )

        default_train_type = TrainType.objects.create(name="Default")
        default_train = Train.objects.create(
            name="IC000",
            cargo_number=6,
            places_in_cargo=60,
            train_type=default_train_type,
        )
        payload = {
            "route": default_route.id,
            "train": default_train.id,
            "departure_time": datetime.now(),
            "arrival_time": datetime.now(),
        }

        response = self.client.post(JOURNEY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        journey = Journey.objects.get(id=response.data["id"])

        for key in payload.keys():
            if key == "route":
                self.assertEqual(payload[key], journey.route.id)
            elif key == "train":
                self.assertEqual(payload[key], journey.train.id)
            else:
                self.assertEqual(payload[key], getattr(journey, key))
