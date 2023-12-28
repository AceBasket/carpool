from rest_framework import serializers
from carpool_app.models import Trip, TripPart, TripRegistration, Car


class TripPartSerializer(serializers.ModelSerializer):
    """Serializer for TripParts model"""
    class Meta:
        """Meta class for TripPartsSerializer"""
        model = TripPart
        exclude = ['slug', 'trip']
        lookup_field = 'slug'

    def create(self, validated_data):
        validated_data['trip'] = Trip.objects.get(
            slug=self.context['view'].kwargs['trip_slug'])
        return super().create(validated_data)


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    trip_parts = TripPartSerializer(read_only=True, many=True)

    class Meta:
        """Meta class for TripSerializer"""
        model = Trip
        exclude = ['slug', 'car']
        lookup_field = 'slug'

    def create(self, validated_data):
        validated_data['car'] = self.context['request'].user.car
        return super().create(validated_data)


class TripRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for TripRegistration model"""

    class Meta:
        """Meta class for TripRegistrationSerializer"""
        model = TripRegistration
        exclude = ['slug']
        lookup_field = 'slug'


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model"""

    class Meta:
        """Meta class for CarSerializer"""
        model = Car
        exclude = ['slug', 'owner']
        lookup_field = 'slug'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
