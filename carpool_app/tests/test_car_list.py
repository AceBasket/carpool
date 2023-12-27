from django.urls import reverse
from carpool_app.models import Car
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model


class CarListTestCase(APITestCase):
    """Test suite for CarViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.driver_user = get_user_model().objects.create_user(
            email='driver@test.com', password='driver')
        self.client.force_authenticate(user=self.driver_user)
        self.url = reverse('car-list')

    def test_create_car(self):
        """Test the api has car creation capability."""
        payload = {
            'license_plate': '123456',
            'type': 'type',
            'color': 'color',
            'num_passenger_seats': 4,
            'owner': self.driver_user.id,
        }
        response = self.client.post(
            self.url,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().license_plate, '123456')
        self.assertEqual(Car.objects.get().type, 'type')
        self.assertEqual(Car.objects.get().color, 'color')
        self.assertEqual(Car.objects.get().num_passenger_seats, 4)

    def test_create_car_unauthenticated(self):
        """Test the api has car creation capability."""
        payload = {
            'license_plate': '123456',
            'type': 'type',
            'color': 'color',
            'num_passenger_seats': 4,
            'owner': self.driver_user.id,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.url,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Car.objects.count(), 0)

    def test_list_cars(self):
        """Test the api has car listing capability."""
        Car.objects.create(
            license_plate='123456',
            type='type',
            color='color',
            num_passenger_seats=4,
            owner=self.driver_user
        )
        response = self.client.get(self.url)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_cars_unauthenticated(self):
        """Test the api has car listing capability."""
        Car.objects.create(
            license_plate='123456',
            type='type',
            color='color',
            num_passenger_seats=4,
            owner=self.driver_user
        )
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
