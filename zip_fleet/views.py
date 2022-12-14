from typing import Type

from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.serializers import Serializer

from zip_fleet.models import Aircraft, Airline
from zip_fleet.serializers import (
    AircraftSerializer,
    AircraftCreateSerializer,
    AirlineSerializer,
    AircraftDetailSerializer,
)


class AirlineViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer


class AircraftViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Aircraft.objects.select_related("airline")

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return AircraftDetailSerializer
        if self.action == "create":
            return AircraftCreateSerializer
        return AircraftSerializer

    @staticmethod
    def _params_to_ints(qs) -> list[int]:
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self) -> QuerySet:
        airlines = self.request.query_params.get("airlines")

        queryset = self.queryset

        if airlines:
            airlines_ids = self._params_to_ints(airlines)
            queryset = queryset.filter(airline__id__in=airlines_ids)

        return queryset.distinct()
