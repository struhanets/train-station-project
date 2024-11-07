from rest_framework import viewsets

from station.models import (
    Train,
    TrainType,
    Station, Route, Crew, Journey, Order, Ticket,
)
from station.serializers import TrainSerializer, TrainTypeSerializer, StationSerializer, RouteSerializer, \
    CrewSerializer, OrderSerializer, TicketSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class JouleViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = CrewSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

