from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from zip_fleet.models import Aircraft

from rest_framework.test import APIClient

from zip_fleet.serializers import AircraftSerializer

AIRCRAFT_URL = reverse("zip_fleet:aircraft-list")


def sample_aircraft(**params):
    defaults = {
        "airline": "TestAirline",
        "seats": 15,
        "passengers": 10
    }
    defaults.update(params)

    return Aircraft.objects.create(**defaults)


class AircraftApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_aircrafts(self):
        sample_aircraft()
        sample_aircraft()

        res = self.client.get(AIRCRAFT_URL)

        movies = Aircraft.objects.all().order_by("id")
        serializer = AircraftSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
