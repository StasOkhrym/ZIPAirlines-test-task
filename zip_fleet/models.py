import math

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Aircraft(models.Model):
    FUEL_TANK_COEFICIENT = 200

    airline = models.CharField(max_length=255, default="ZipAirline")
    seats = models.IntegerField(validators=[MinValueValidator(1)])
    passengers = models.IntegerField()

    @property
    def fuel_capacity(self) -> int:
        return self.FUEL_TANK_COEFICIENT * self.id

    @property
    def fuel_consumption(self) -> int | float:
        return (math.log(self.id) * 0.08) + (self.passengers * 0.002)

    @staticmethod
    def validate_passengers(seats, passengers, error_to_raise):
        if not (0 <= passengers <= seats):
            raise error_to_raise(
                {
                    "passengers": "please enter correct passengers count"
                }
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
