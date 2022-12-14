from django.urls import path, include
from rest_framework import routers

from zip_fleet.views import AircraftViewSet

router = routers.DefaultRouter()
router.register("aircrafts", AircraftViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "zip_fleet"
