import datetime
from carpool_app.models import Car, Trip, TripPart, TripRegistration
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status


class TripRegistrationDetailTestCase(APITestCase):
    """Test suite for TripRegistrationViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        )
        self.client.force_authenticate(user=self.user)
        car = Car.objects.create(license_plate='123456',
                                 owner=self.user,
                                 num_passenger_seats=4,
                                 slug='123456')
        self.trip = Trip.objects.create(date=datetime.date(2020, 12, 12),
                                        car=car,
                                        slug='123456_2020-12-12')
        self.trip2 = Trip.objects.create(date=datetime.date(2020, 12, 13),
                                         car=car,
                                         slug='123456_2020-12-12-v2')
        self.trip_registration = TripRegistration.objects.create(
            user=self.user,
            trip=self.trip,
            slug='test2'
        )
        self.url = reverse('registration-detail',
                           kwargs={'slug': self.trip_registration.slug})

    def test_delete_trip_registration(self):
        """Test the api has trip_registration delete capability."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TripRegistration.objects.count(), 0)

    def test_delete_trip_registration_unauthenticated(self):
        """Test the api has trip_registration delete capability."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(TripRegistration.objects.count(), 1)

    def test_retrieve_trip_registration(self):
        """Test the api has trip_registration retrieve capability."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['trip'], self.trip.id)

    def test_update_trip_registration(self):
        """Test the api has trip_registration update capability."""
        payload = {
            'user': self.user.id,
            'trip': self.trip2.id,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['trip'], self.trip2.id)

    def test_update_trip_registration_unauthenticated(self):
        """Test the api has trip_registration update capability."""
        self.client.force_authenticate(user=None)
        payload = {
            'user': self.user.id,
            'trip': self.trip2.id,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_trip_registration(self):
        """Test the api has trip_registration partial_update capability."""
        payload = {
            'trip': self.trip2.id,
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['trip'], self.trip2.id)

    def test_partial_update_trip_registration_unauthenticated(self):
        """Test the api has trip_registration partial_update capability."""
        self.client.force_authenticate(user=None)
        payload = {
            'trip': self.trip2.id,
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
