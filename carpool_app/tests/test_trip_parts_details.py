import datetime
from carpool_app.models import Car, Trip, TripPart
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class TripPartDetailTestCase(APITestCase):
    """Test suite for TripPartViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        )
        self.client.force_authenticate(user=self.user)
        self.trip = Trip.objects.create(date=datetime.date(2020, 12, 12),
                                        car=Car.objects.create(license_plate='123456',
                                                               owner=self.user,
                                                               num_passenger_seats=4))
        self.trip_part = TripPart.objects.create(trip=self.trip,
                                                 departure_time=datetime.time(
                                                     12, 0),
                                                 distance=100,
                                                 duration=100,
                                                 fee=100,
                                                 starting_point='A',
                                                 ending_point='B')
        self.assertEqual(self.trip_part.slug, "123456_2020-12-12_at_12h0")
        self.url = reverse('trip_part-detail',
                           kwargs={'trip_slug': self.trip.slug, 'slug': self.trip_part.slug})

    def test_retrieve_trip_part(self):
        """Test the api has trip_part retrieve capability."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['trip'], self.trip.id)
        self.assertEqual(response.data['departure_time'], '12:00:00')
        self.assertEqual(response.data['distance'], 100)
        self.assertEqual(response.data['duration'], 100)
        self.assertEqual(response.data['fee'], 100)
        self.assertEqual(response.data['starting_point'], 'A')
        self.assertEqual(response.data['ending_point'], 'B')

    def test_update_trip_part(self):
        """Test the api has trip_part update capability."""
        payload = {
            'trip': self.trip.id,
            'departure_time': '12:00',
            'distance': 100,
            'duration': 100,
            'fee': 100,
            'starting_point': 'A',
            'ending_point': 'B',
        }
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TripPart.objects.count(), 1)
        self.assertEqual(TripPart.objects.get().trip.id, self.trip.id)
        self.assertEqual(TripPart.objects.get(
        ).departure_time, datetime.time(12, 0))
        self.assertEqual(TripPart.objects.get().distance, 100)
        self.assertEqual(TripPart.objects.get().duration, 100)
        self.assertEqual(TripPart.objects.get().fee, 100)
        self.assertEqual(TripPart.objects.get().starting_point, 'A')
        self.assertEqual(TripPart.objects.get().ending_point, 'B')

    def test_delete_trip_part(self):
        """Test the api has trip_part delete capability."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TripPart.objects.count(), 0)

    def test_retrieve_trip_part_unauthenticated(self):
        """Test the api has trip_part retrieve capability."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_trip_part_unauthenticated(self):
        """Test the api has trip_part update capability."""
        payload = {
            'trip': self.trip.id,
            'departure_time': '12:00',
            'distance': 100,
            'duration': 100,
            'fee': 100,
            'starting_point': 'A',
            'ending_point': 'B',
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_trip_part_unauthenticated(self):
        """Test the api has trip_part delete capability."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
