from django.test import TestCase

from zip_fleet.models import Aircraft

from rest_framework.test import APIClient


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

