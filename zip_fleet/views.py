from rest_framework import mixins, viewsets

from zip_fleet.models import Aircraft
from zip_fleet.serializers import AircraftSerializer, AircraftCreateSerializer


class AircraftViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Aircraft.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return AircraftCreateSerializer
        return AircraftSerializer
