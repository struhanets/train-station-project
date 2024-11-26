from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import TrainType
from station.serializers import TrainTypeSerializer

TRAIN_TYPE_URL = reverse("station:traintype-list")


def sample_train_type(**params):
    default = {"name": "Default"}

    default.update(params)
    return TrainType.objects.create(**default)


class TrainTypeUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TRAIN_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TrainAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test111",
        )
        self.client.force_authenticate(self.user)

    def test_trains_list(self):
        sample_train_type()
        response = self.client.get(TRAIN_TYPE_URL)
        train_types = TrainType.objects.all()
        serializer = TrainTypeSerializer(train_types, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["results"], serializer.data)

    def test_train_type_create(self):
        payload = {"name": "default"}

        response = self.client.post(TRAIN_TYPE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        train_type = TrainType.objects.get(id=response.data["id"])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(train_type, key))
