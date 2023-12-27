from rest_framework import serializers
from django.contrib.auth.models import Group
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
    """Serializer for TripParts model"""
    class Meta:
        """Meta class for TripPartsSerializer"""
        model = TripPart
        fields = ['id', 'departure_time', 'distance', 'duration', 'fee',
                  'starting_point', 'ending_point', 'registrations', 'trip']


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    trip_parts = TripPartSerializer(read_only=True, many=True)

    class Meta:
        """Meta class for TripSerializer"""
        model = Trip
        fields = ['id', 'date', 'car', 'trip_parts']


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
        fields = ['id', 'type', 'color', 'license_plate',
                  'owner', 'num_passenger_seats']
