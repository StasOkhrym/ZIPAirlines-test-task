from rest_framework import serializers

from zip_fleet.models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aircraft
        fields = (
            "id"
            "airline"
            "seats"
            "passengers"
            "fuel_capacity"
            "fuel_consumption"
        )
