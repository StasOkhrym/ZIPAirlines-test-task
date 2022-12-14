from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from zip_fleet.models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aircraft
        fields = (
            "id",
            "airline",
            "seats",
            "passengers",
            "fuel_capacity",
            "fuel_consumption",
            "flight_time"
        )


class AircraftCreateSerializer(AircraftSerializer):

    def create(self, validated_data) -> Aircraft:
        aircrafts = Aircraft.objects.filter(airline=validated_data["airline"])

        if aircrafts > 10:
            raise ValidationError(
                {
                    "company_fleet":
                    "company can have no more than 10 aircrafts"
                }
            )

        return super(AircraftCreateSerializer, self).create(validated_data=validated_data)

