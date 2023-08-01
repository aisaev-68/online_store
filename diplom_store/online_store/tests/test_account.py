from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from account.serializers import UserSerializer, UserAvatarSerializer, UserPasswordChangeSerializer

# Assuming you have all other required imports and setup for your project

class AccountUserAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_account_user_api_view(self):
        url = reverse('account-user-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserAvatarSerializer(self.user)
        self.assertEqual(response.data, serializer.data)


class RegisterViewTest(APITestCase):
    def test_register_view_valid_data(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_invalid_data(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(username='newuser').exists())


class MyLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_my_login_view_valid_credentials(self):
        url = reverse('my-login')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile')  # Assuming successful login redirects to '/profile'

    def test_my_login_view_invalid_credentials(self):
        url = reverse('my-login')
        data = {
            'username': 'testuser',
            'password': 'invalidpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')  # Assuming unsuccessful login redirects to '/login'

    def test_my_login_view_authenticated_user_redirect(self):
        url = reverse('my-login')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile')  # Assuming authenticated user redirects to '/profile'


# Create tests for other views in a similar way

# Remember to include the URL names used in the tests in your Django project's URL configuration.
