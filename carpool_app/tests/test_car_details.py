from django.urls import reverse
from carpool_app.models import Car
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model


class CarDetailTestCase(APITestCase):
    """Test suite for CarViewSet"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.driver_user = get_user_model().objects.create_user(
            email='driver@test.com', password='driver')
        self.client.force_authenticate(user=self.driver_user)
        self.car = Car.objects.create(license_plate='123456',
                                      type='type',
                                      color='color',
                                      num_passenger_seats=4,
                                      owner=self.driver_user)
        self.assertEqual(self.car.slug, self.car.license_plate)
        self.url = reverse('car-detail', kwargs={'slug': self.car.slug})

    def test_retrieve_car(self):
        """Test the api has car retrieve capability."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['license_plate'], '123456')
        self.assertEqual(response.data['type'], 'type')
        self.assertEqual(response.data['color'], 'color')
        self.assertEqual(response.data['num_passenger_seats'], 4)

    def test_update_car(self):
        """Test the api has car update capability."""
        payload = {
            'license_plate': '123456',
            'type': 'type',
            'color': 'color',
            'num_passenger_seats': 4,
            'owner': self.driver_user.id,
        }
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().license_plate, '123456')
        self.assertEqual(Car.objects.get().type, 'type')
        self.assertEqual(Car.objects.get().color, 'color')
        self.assertEqual(Car.objects.get().num_passenger_seats, 4)

    def test_delete_car(self):
        """Test the api has car delete capability."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)

    def test_retrieve_car_unauthorized(self):
        """Test the api has car retrieve capability."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_car_unauthorized(self):
        """Test the api has car update capability."""
        payload = {
            'license_plate': '123456',
            'type': 'type',
            'color': 'color',
            'num_passenger_seats': 4,
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_car_unauthorized(self):
        """Test the api has car delete capability."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
