from rest_framework import viewsets
from rest_framework import permissions
from carpool_app.models import Trip, TripPart, TripRegistration, Car
from carpool_app.producer import publish
from carpool_app.serializers import TripSerializer, TripPartSerializer, TripRegistrationSerializer, CarSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from user.models import User


class IsDriver(permissions.BasePermission):
    """
    Custom permission to only allow drivers to create trips and trip parts.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.car.exists()
        return True


class IsTripOwnedBy(permissions.BasePermission):
    """
    Custom permission to only allow drivers that created the trip to create trip parts.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            trip_id = view.kwargs['pk']
            try:
                trip = Trip.objects.get(pk=trip_id)
            except Trip.DoesNotExist:
                return False
            return request.user.car == trip.car
        else:
            return True


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    lookup_field = 'slug'

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
            source = request.GET.get('source')
            destination = request.GET.get('destination')
            trips = self.get_by_source_and_destination(source, destination)
            return Response(TripSerializer(trips, many=True).data)
        return super().list(request, *args, **kwargs)

    def get_by_source_and_destination(self, source=None, destination=None):
        """
        Get trip parts by source and destination
        """
        trips = Trip.objects.prefetch_related('trip_parts')
        if source:
            trips = trips.filter(trip_parts__starting_point=source)
        if destination:
            trips = trips.filter(trip_parts__ending_point=destination)
        return trips

    def destroy(self, request, pk=None):
        publish('trip_deleted', pk)
        return super().destroy(request, pk)


class TripPartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trip parts to be viewed or edited.
    """

    queryset = TripPart.objects.all()
    serializer_class = TripPartSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver, IsTripOwnedBy]
    lookup_field = 'slug'


class TripRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trip registrations to be viewed or edited.
    """

    queryset = TripRegistration.objects.all()
    serializer_class = TripRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


# class IsAllowedToReview(permissions.BasePermission):
#     """
#     Custom permission to only allow users that have been in a trip with the user to review them.
#     """

#     def has_permission(self, request, view):
#         reviewed_user_id = view.kwargs['reviewee']
#         reviewed_user = User.objects.get(pk=reviewed_user_id)
#         trip_id = view.kwargs['trip']
#         trip = Trip.objects.get(pk=trip_id)
#         # can't review yourself and need to have been on the trip (as passenger or driver) + same conditions for user reviewed
#         return request.user != reviewed_user and (request.user in trip.passengers.all() or request.user == trip.car.driver) and (reviewed_user in trip.passengers.all() or reviewed_user == trip.car.driver)


class IsCarOwner(permissions.BasePermission):
    """
    Custom permission to only allow users that own a car to manage that car.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.car == obj


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed or edited.
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCarOwner]
    lookup_field = 'slug'
