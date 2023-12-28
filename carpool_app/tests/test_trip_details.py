import datetime
from carpool_app.models import Car, Trip
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class TripDetailTestCase(APITestCase):
    """Test suite for TripViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        )
        self.trip = Trip.objects.create(date=datetime.date(2020, 12, 12),
                                        car=Car.objects.create(license_plate='123456',
                                                               owner=self.user,
                                                               num_passenger_seats=4)
                                        )
        self.assertEqual(self.trip.slug, "123456_2020-12-12")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('trip-detail', kwargs={'slug': self.trip.slug})

    def test_retrieve_trip(self):
        """Test the api has trip retrieve capability."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], '2020-12-12')

    def test_update_trip(self):
        """Test the api has trip update capability."""
        payload = {
            'date': '2020-12-21',
            'car': self.trip.car.id,
        }
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Trip.objects.get().date, datetime.date(2020, 12, 21))
        self.assertEqual(Trip.objects.get().car, self.trip.car)

    def test_delete_trip(self):
        """Test the api has trip delete capability."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Trip.objects.count(), 0)

    def test_retrieve_trip_unauthenticated(self):
        """Test the api has trip retrieve capability."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_trip_unauthenticated(self):
        """Test the api has trip update capability."""
        payload = {
            'date': '2020-12-21',
            'car': self.trip.car.id,
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_trip_unauthenticated(self):
        """Test the api has trip delete capability."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
