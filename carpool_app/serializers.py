from rest_framework import serializers
from carpool_app.models import Trip, TripPart, TripRegistration, Review, Car


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
    fee = serializers.IntegerField(required=False)

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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""

    class Meta:
        """Meta class for ReviewSerializer"""
        model = Review
        fields = ['id', 'score', 'content', 'reviewer', 'reviewee', 'trip']


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model"""

    class Meta:
        """Meta class for CarSerializer"""
        model = Car
        fields = ['id', 'type', 'color', 'license_plate',
                  'owner', 'num_passenger_seats']
