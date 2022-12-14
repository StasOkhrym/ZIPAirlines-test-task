from django.urls import path, include
from rest_framework import routers

from zip_fleet.views import AircraftViewSet, AirlineViewSet

router = routers.DefaultRouter()
router.register("airlines", AirlineViewSet)
router.register("aircrafts", AircraftViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "zip_fleet"
