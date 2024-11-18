from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from station.models import (
    Train,
    TrainType,
    Station,
    Route,
    Crew,
    Journey,
    Order,
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
    JourneyRetrieveSerializer,
    OrderListSerializer,
)


@extend_schema(
    tags=["Trains"],
    description="Endpoints to manage trains in the train system. "
                "You can create, list, retrieve, update, "
                "or delete train data."
)
class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = self.queryset.select_related()

        train_type = self.request.query_params.get("train_type")
        if train_type:
            train_type_ids = [int(train_type_id) for train_type_id in train_type.split(",")]
            queryset = queryset.filter(train_type__id__in=train_type_ids)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="train_type",
                type={"type": "array", "items": {"type": "number"}},
                description="filter by train type ids (ex. ?train_type=1,2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of trains and filter them by train_types"""
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Train_types"],
    description="Endpoints to manage train_types in the train system. "
                "You can create, list, retrieve, update, "
                "or delete train_type data."
)
class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    authentication_classes = (TokenAuthentication,)


@extend_schema(
    tags=["Stations"],
    description="Endpoints to manage stations. "
                "You can create, list, retrieve, update, "
                "or delete station data."
)
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    authentication_classes = (TokenAuthentication,)


@extend_schema(
    tags=["Routes"],
    description="Endpoints to manage routes. "
                "You can create, list, retrieve, update, "
                "or delete route data."
)
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    authentication_classes = (TokenAuthentication,)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                type={"type": "string"},
                description="filter source stations (ex. ?source=Kyiv)",
            ),
            OpenApiParameter(
                name="destination",
                type={"type": "string"},
                description="filter source stations (ex. ?source=Krakow)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Filtering source or destination by stations name"""
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Crews"],
    description="Endpoints to manage crews in the train system. "
                "You can create, list, retrieve, update, "
                "or delete crew data."
)
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    authentication_classes = (TokenAuthentication,)


@extend_schema(
    tags=["Journeys"],
    description="Endpoints to manage journeys. "
                "You can create, list, retrieve, update, "
                "or delete journey data."
)
class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JourneyRetrieveSerializer

        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('list', 'retrieve'):
            queryset = queryset.select_related('train', 'route')

        return queryset


@extend_schema(
    tags=["Orders"],
    description="Endpoints to manage orders. "
                "You can create, list, retrieve, update, "
                "or delete order data."
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)

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
