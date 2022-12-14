import math
import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from zip_fleet.models import Aircraft, Airline

from rest_framework.test import APIClient

from zip_fleet.serializers import AircraftSerializer, AircraftDetailSerializer

AIRCRAFT_URL = reverse("zip_fleet:aircraft-list")


def sample_airline(**params):
    defaults = {"name": f"TestAirline{random.randint(1,100)}"}
    defaults.update(**params)
    return Airline.objects.create(**defaults)


def sample_aircraft(**params):
    defaults = {"airline": sample_airline(), "seats": 15, "passengers": 10}
    defaults.update(params)

    return Aircraft.objects.create(**defaults)


def detail_url(aircraft_id):
    return reverse("zip_fleet:aircraft-detail", args=[aircraft_id])


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

    def test_filter_aircrafts_by_airline(self):
        airline1 = Airline.objects.create(name="Airline1")
        airline2 = Airline.objects.create(name="Airline2")

        aircraft1 = sample_aircraft()
        aircraft2 = sample_aircraft()
        aircraft3 = sample_aircraft()

        aircraft1.airline = airline1
        aircraft2.airline = airline1
        aircraft3.airline = airline2
        aircraft1.save()
        aircraft2.save()
        aircraft3.save()

        res = self.client.get(AIRCRAFT_URL, {"airlines": f"{airline1.id}"})

        serializer1 = AircraftSerializer(aircraft1)
        serializer2 = AircraftSerializer(aircraft2)
        serializer3 = AircraftSerializer(aircraft3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_aircraft_detail(self):
        aircraft = sample_aircraft()

        url = detail_url(aircraft.id)
        res = self.client.get(url)

        serializer = AircraftDetailSerializer(aircraft)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_aircraft_properties_calculated_correctly(self):
        aircraft = sample_aircraft()
        fuel_tank_coeficient = 200

        fuel_capacity = aircraft.id * fuel_tank_coeficient
        fuel_consumption = round(
            (math.log(aircraft.id) * 0.08) + (aircraft.passengers * 0.002), 3
        )
        flight_time = round(fuel_capacity / fuel_consumption, 2)

        serializer = AircraftDetailSerializer(aircraft)

        self.assertEqual(serializer.data["fuel_capacity"], fuel_capacity)
        self.assertEqual(serializer.data["fuel_consumption"], fuel_consumption)
        self.assertEqual(serializer.data["flight_time"], flight_time)
