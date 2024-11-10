from rest_framework import viewsets

from station.models import (
    Train,
    TrainType,
    Station,
    Route,
    Crew,
    Journey,
    Order,
    Ticket
)

from station.serializers import (
    TrainSerializer,
    TrainTypeSerializer,
    StationSerializer,
    RouteSerializer,
    CrewSerializer,
    OrderSerializer,
    TicketSerializer,
    JourneySerializer, TicketDetailSerializer, TicketListSerializer, TrainListSerializer, RouteListSerializer
)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TrainListSerializer

        return TrainSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            return queryset.select_related()

        return queryset


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer

        return RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'retrieve':
            return TicketDetailSerializer

        return TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            return queryset.select_related()

        return queryset
