from rest_framework import mixins, viewsets

from zip_fleet.models import Aircraft
from zip_fleet.serializers import AircraftSerializer


class AircraftViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
