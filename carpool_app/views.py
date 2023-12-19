from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import Group
from carpool_app.models import User, Trip, TripPart, TripRegistration, Car
from rest_framework.response import Response
from carpool_app.serializers import UserSerializer, GroupSerializer, TripSerializer, TripPartSerializer, TripRegistrationSerializer, CarSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

   
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]


class TripRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trip registrations to be viewed or edited.
    """

    queryset = TripRegistration.objects.all()
    serializer_class = TripRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class TripList(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer



class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed or edited.
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

