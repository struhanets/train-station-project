from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Train, TrainType
from station.serializers import TrainSerializer

TRAIN_URL = reverse("station:train-list")


def sample_train(**params) -> Train:
    default_train_type = TrainType.objects.create(
        name="Default"
    )
    defaults = {
        "name": "IC000",
        "cargo_number": 6,
        "places_in_cargo": 60,
        "train_type": default_train_type
    }
    defaults.update(params)
    return Train.objects.create(**defaults)


class TrainUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TRAIN_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TrainAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test", password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_trains_list(self):
        sample_train()
        response = self.client.get(TRAIN_URL)
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["results"], serializer.data)

    def test_train_filter_by_type(self):
        train = sample_train()

        response = self.client.get(TRAIN_URL, {"train_type": f"{train.train_type.id}"})

        serializer = TrainSerializer(train)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, response.data["results"])

    def test_trains_create(self):
        default_train_type = TrainType.objects.create(
            name="Default1"
        )
        payload = {
            "name": "IC111",
            "cargo_number": 4,
            "places_in_cargo": 50,
            "train_type": default_train_type.id
        }

        response = self.client.post(TRAIN_URL, payload)

        train = Train.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            if key == "train_type":
                self.assertEqual(payload[key], train.train_type.id)
            else:
                self.assertEqual(payload[key], getattr(train, key))