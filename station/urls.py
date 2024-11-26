from django.urls import path, include
from rest_framework import routers

from station.views import (
    TrainViewSet,
    TrainTypeViewSet,
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    JourneyViewSet,
    OrderViewSet,
)

app_name = "station"

router = routers.DefaultRouter()
router.register("trains", TrainViewSet)
router.register("train_types", TrainTypeViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)


urlpatterns = [path("", include(router.urls))]
