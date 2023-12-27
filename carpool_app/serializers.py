from rest_framework import serializers
from carpool_app.models import Trip, TripPart, TripRegistration, Car


class TripPartSerializer(serializers.ModelSerializer):
    """Serializer for TripParts model"""
    class Meta:
        """Meta class for TripPartsSerializer"""
        model = TripPart
        exclude = ['slug']
        lookup_field = 'slug'
        # fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    trip_parts = TripPartSerializer(read_only=True, many=True)

    class Meta:
        """Meta class for TripSerializer"""
        model = Trip
        # fields = '__all__'
        exclude = ['slug']
        lookup_field = 'slug'


class TripRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for TripRegistration model"""

    class Meta:
        """Meta class for TripRegistrationSerializer"""
        model = TripRegistration
        # fields = '__all__'
        exclude = ['slug']
        lookup_field = 'slug'


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model"""

    def create(self, validated_data):
        # slugify license plate
        validated_data['slug'] = validated_data['license_plate']
        return super().create(validated_data)

    class Meta:
        """Meta class for CarSerializer"""
        model = Car
        exclude = ['slug']
        lookup_field = 'slug'
