from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class UserCreateTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('user-create')
        data = {
            'email': 'test@example.com',
            'phone_number': '+123456789',
            'surname': 'John Doe',
            # Add any additional fields required for user creation
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        # Add additional assertions if necessary


class UserAuthorizationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')

    def test_user_authorization_success(self):
        url = reverse('user-authorization')
        data = {
            'email_or_phone_number': 'test@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Сообщение', response.data)
        # Add additional assertions if necessary

    def test_user_authorization_invalid_credentials(self):
        url = reverse('user-authorization')
        data = {
            'email_or_phone_number': 'test@example.com',
            'password': 'wrongpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Сообщение', response.data)
        # Add additional assertions if necessary


class UserLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')

    def test_user_logout(self):
        url = reverse('user-logout')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Сообщение', response.data)
        # Add additional assertions if necessary
