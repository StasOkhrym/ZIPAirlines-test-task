import math
from typing import Type

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Airline(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Aircraft(models.Model):
    FUEL_TANK_COEFICIENT = 200

    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    seats = models.IntegerField(validators=[MinValueValidator(1)])
    passengers = models.IntegerField()

    @property
    def fuel_capacity(self) -> int:
        return self.FUEL_TANK_COEFICIENT * self.id

    @property
    def fuel_consumption(self) -> int | float:
        fuel_consumption = (math.log(self.id) * 0.08) + (
            self.passengers * 0.002
        )
        return round(fuel_consumption, 3)

    @property
    def flight_time(self) -> int | float:
        flight_time = self.fuel_capacity / self.fuel_consumption
        return round(flight_time, 2)

    @staticmethod
    def validate_passengers(
        seats: int, passengers: int, error_to_raise: Type[Exception]
    ) -> None:
        if not (0 <= passengers <= seats):
            raise error_to_raise(
                {"passengers": "please enter correct passengers count"}
            )

    def clean(self):
        Aircraft.validate_passengers(
            self.seats,
            self.passengers,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Aircraft, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.airline} aircraft (seats: {self.seats}, passengers: {self.passengers})"
