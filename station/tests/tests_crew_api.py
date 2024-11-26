from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Crew
from station.serializers import CrewSerializer

CREW_URL = reverse("station:crew-list")


def sample_crew(**params):
    default = {
        "first_name": "John",
        "last_name": "Smith"
    }
    default.update(params)
    return Crew.objects.create(**default)


class CrewUnAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(CREW_URL)
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
        sample_crew()
        response = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["results"], serializer.data)

    def test_trains_create(self):
        payload = {
            "first_name": "John",
            "last_name": "Smith"
        }

        response = self.client.post(CREW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        crew = Crew.objects.get(id=response.data["id"])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(crew, key))
