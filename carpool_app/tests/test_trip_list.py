import datetime
from carpool_app.models import Car, Trip
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class TripListTestCase(APITestCase):
    """Test suite for TripViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('trip-list')
        self.car = Car.objects.create(license_plate='123456',
                                      owner=self.user,
                                      num_passenger_seats=4,
                                      slug='123456')

    def test_create_trip(self):
        """Test the api has trip create capability."""
        payload = {
            'date': '2020-12-12',
            'car': self.car.id,
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Trip.objects.get().date, datetime.date(2020, 12, 12))
        self.assertEqual(Trip.objects.get().car, self.car)

    def test_create_trip_with_invalid_date(self):
        """Test the api has trip create capability."""
        payload = {
            'date': '2020-12-32',
            'car': self.car.id,
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Trip.objects.count(), 0)

    def test_create_trip_unauthaurized(self):
        """Test the api has trip create capability."""
        payload = {
            'date': '2020-12-12',
            'car': self.car.id,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Trip.objects.count(), 0)

    def test_list_cars(self):
        """Test the api has car list capability."""
        trip = Trip.objects.create(date='2020-12-12', car=self.car)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_cars_unauthenticated(self):
        """Test the api has car list capability."""
        trip = Trip.objects.create(date='2020-12-12', car=self.car)
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
