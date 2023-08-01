from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from account.serializers import UserAvatarSerializer


class AccountUserAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@user.ru',
            password='user12345',
            phone="89305484111",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
            is_staff=True,
        )
        self.client.login(username='user', password='user12345')

    def test_get_account_user_api_view(self):
        url = reverse('account:account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserAvatarSerializer(self.user)
        self.assertEqual(response.data, serializer.data)


class RegisterViewTest(APITestCase):
    def test_register_view_valid_data(self):
        url = reverse('register')
        data = {
            'username': 'user',
            'email': 'user@user.ru',
            'phone': "89305484111",
            'password1': 'user12345',
            'password2': 'user12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username='user').exists())

    def test_register_view_invalid_data(self):
        url = reverse('frontend:register')
        data = {
            'username': 'user',
            'email': 'user@user.ru',
            'phone': "89305484111",
            'password1': 'user123',
            'password2': 'user12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(username='user').exists())


class MyLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@user.ru',
            password='user12345',
            phone="89305484111",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
            is_staff=True,
        )

    def test_my_login_view_valid_credentials(self):
        url = reverse('frontend:login')
        data = {
            'username': 'user',
            'password': 'user12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile')  # Assuming successful login redirects to '/profile'

    def test_my_login_view_invalid_credentials(self):
        url = reverse('frontend:login')
        data = {
            'username': 'user',
            'password': 'password12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')  # Assuming unsuccessful login redirects to '/login'

    def test_my_login_view_authenticated_user_redirect(self):
        url = reverse('frontend:login')
        self.client.login(username='user', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile')  # Assuming authenticated user redirects to '/profile'
