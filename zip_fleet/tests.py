import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from zip_fleet.models import Aircraft, Airline

from rest_framework.test import APIClient

from zip_fleet.serializers import AircraftSerializer

AIRCRAFT_URL = reverse("zip_fleet:aircraft-list")


def sample_airline(**params):
    defaults = {
        "name": f"TestAirline{random.randint(1,100)}"
    }
    defaults.update(**params)
    return Airline.objects.create(**defaults)


def sample_aircraft(**params):
    defaults = {"airline": sample_airline(), "seats": 15, "passengers": 10}
    defaults.update(params)

    return Aircraft.objects.create(**defaults)


class AircraftApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_aircrafts(self):
        sample_aircraft()
        sample_aircraft()

        res = self.client.get(AIRCRAFT_URL)

        aircrafts = Aircraft.objects.all().order_by("id")
        serializer = AircraftSerializer(aircrafts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
