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
    JourneySerializer,
    RouteListSerializer,
    JourneyRetrieveSerializer, OrderListSerializer,
)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related()

        train_type = self.request.query_params.get("train_type")
        if train_type:
            train_type_ids = [int(train_type_id) for train_type_id in train_type.split(",")]
            queryset = queryset.filter(train_type__id__in=train_type_ids)

        return queryset


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.select_related('source', 'destination')

            source = self.request.query_params.get("source")
            destination = self.request.query_params.get("destination")

            if source:
                queryset = queryset.filter(source__name__icontains=source)
            if destination:
                queryset = queryset.filter(destination__name__icontains=destination)

        return queryset


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JourneyRetrieveSerializer

        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related('train', 'route')

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == 'list':
            queryset = queryset.prefetch_related(
                "tickets__train",
                "tickets__journey",
                "tickets__journey__route"
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == 'list':
            serializer = OrderListSerializer

        return serializer
