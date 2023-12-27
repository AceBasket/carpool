import datetime
from carpool_app.models import Car, Trip, TripRegistration
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status


class TripRegistrationListTestCase(APITestCase):
    """Test suite for TripRegistrationViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('registration-list')

    def test_create_trip_registration(self):
        """Test the api has trip_registration create capability."""
        trip_id = Trip.objects.create(date=datetime.date(2020, 12, 12),
                                      car=Car.objects.create(license_plate='123456',
                                                             owner=self.user,
                                                             num_passenger_seats=4,
                                                             slug='123456'),
                                      slug='123456_2020-12-12').id
        payload = {
            'user': self.user.id,
            'trip': trip_id,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['trip'], 1)

    def test_list_trip_registrations(self):
        """Test the api has trip_registration list capability."""
        TripRegistration.objects.create(
            user=self.user,
            trip=Trip.objects.create(date=datetime.date(2020, 12, 12),
                                     car=Car.objects.create(license_plate='123456',
                                                            owner=self.user,
                                                            num_passenger_seats=4,
                                                            slug='123456'),
                                     slug='123456_2020-12-12'),
            slug='test'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_trip_registration_unauthenticated(self):
        """Test the api has trip_registration create capability."""
        self.client.force_authenticate(user=None)
        trip_id = Trip.objects.create(date=datetime.date(2020, 12, 12),
                                      car=Car.objects.create(license_plate='123456',
                                                             owner=self.user,
                                                             num_passenger_seats=4,
                                                             slug='123456'),
                                      slug='123456_2020-12-12').id
        payload = {
            'user': self.user.id,
            'trip': trip_id,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(TripRegistration.objects.count(), 0)

    def test_list_trip_registrations_unauthenticated(self):
        """Test the api has trip_registration list capability."""
        self.client.force_authenticate(user=None)
        TripRegistration.objects.create(
            user=self.user,
            trip=Trip.objects.create(date=datetime.date(2020, 12, 12),
                                     car=Car.objects.create(license_plate='123456',
                                                            owner=self.user,
                                                            num_passenger_seats=4,
                                                            slug='123456'),
                                     slug='123456_2020-12-12'),
            slug='test'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
