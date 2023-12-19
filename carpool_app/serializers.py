from django.contrib.auth.models import Group
from rest_framework import serializers
from carpool_app.models import User, Trip, TripPart, TripRegistration, Car


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        """Meta class for UserSerializer"""
        model = User
        fields = ['id', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""
    class Meta:
        """Meta class for GroupSerializer"""
        model = Group
        fields = ['url', 'name']


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""

    class Meta:
        """Meta class for TripSerializer"""
        model = Trip
        fields = ['id', 'date', 'car']


class TripPartSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    trip = TripSerializer()

    class Meta:
        """Meta class for TripSerializer"""
        model = TripPart
        fields = ['id', 'departure_time', 'distance', 'duration', 'fee',
                  'starting_point', 'ending_point', 'registrations', 'trip']

    def create(self, validated_data):
        trip_data = validated_data.pop('trip')
        trip = Trip.objects.create(**trip_data)
        trip_part = TripPart.objects.create(trip=trip, **validated_data)
        return trip_part


class TripRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for TripRegistration model"""

    class Meta:
        """Meta class for TripRegistrationSerializer"""
        model = TripRegistration
        fields = ['id', 'user', 'trip']


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model"""

    class Meta:
        """Meta class for CarSerializer"""
        model = Car
        fields = ['id', 'owner', 'make', 'model', 'year', 'num_passenger_seats']