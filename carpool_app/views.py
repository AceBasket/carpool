from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from carpool_app.models import Trip, TripPart, TripRegistration, Review, Car
from carpool_app.serializers import TripSerializer, TripPartSerializer, TripRegistrationSerializer, ReviewSerializer, CarSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name='source', description='A string corresponding to the wanted starting point', required=False, type=str),
            OpenApiParameter(
                name='destination', description='A string corresponding to the wanted ending point', required=False, type=str),
        ],
    )
    def list(self, request, *args, **kwargs):
        if (request.GET.get('source') and request.GET.get('destination')):
            return self.get_by_source_and_destination(request, request.GET.get('source'), request.GET.get('destination'))
        return super().list(request, *args, **kwargs)

    def get_by_source_and_destination(self, request, source, destination):
        """
        Get trip parts by source and destination
        """
        trips = Trip.objects.get_by_source_and_destination(source, destination)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


class TripPartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trip parts to be viewed or edited.
    """

    queryset = TripPart.objects.all()
    serializer_class = TripPartSerializer
    # permission_classes = [permissions.IsAuthenticated]


class TripRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trip registrations to be viewed or edited.
    """

    queryset = TripRegistration.objects.all()
    serializer_class = TripRegistrationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     return request.user.reviewer_id.all()
    #     return super().list(request, *args, **kwargs)


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed or edited.
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    # permission_classes = [permissions.IsAuthenticated]
