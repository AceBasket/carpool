from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
# Create your tests here.


class UsersManagersTests(TestCase):
    """Test custom user model"""

    def test_create_user(self):
        """Test creating a new user"""
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email="")
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


class AuthTestCase(APITestCase):
    """Test suite for authentication"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

    def test_register(self):
        """Test the api has user register capability."""
        payload = {
            'email': 'test@test.com',
            'password': 'test',
        }

        response = self.client.post(
            reverse('register'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_generate_otp(self):
        """Test the api has user generate OTP and auth URL capability."""
        user_id = get_user_model().objects.create_user(
            email='test@test.com',
            password='test'
        ).id
        payload = {
            'email': 'test@test.com',
            'user_id': user_id,
        }

        response = self.client.post(
            reverse('generate_otp'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['base32'])
        self.assertTrue(response.data['otpauth_url'])
