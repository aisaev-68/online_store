from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from account.models import User
from account.serializers import UserAvatarSerializer


class AccountUserAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@user.ru',
            password='user12345',
            phone="89305484911",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович",
        )
        self.client.login(username='user', password='user12345')

    def tearDown(self):
        self.user.delete()


    def test_get_account_user_api_view(self):
        url = reverse('account:account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserAvatarSerializer(self.user)
        self.assertEqual(response.data, serializer.data)


class RegisterViewTest(APITestCase):
    def setUp(self):
        Group.objects.get_or_create(name="Clients")
    def tearDown(self):
        # Delete the user created during the test
        User.objects.filter(username='user').delete()
        Group.objects.filter(name="Clients").delete()
        
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
        url = reverse('register')
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
            surname="Иванович"
        )

    def tearDown(self):
        self.user.delete()

    def test_my_login_view_valid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'user',
            'password': 'user12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/account/')  # Assuming successful login redirects to '/profile'

    def test_my_login_view_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'user',
            'password': 'password12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login/')  # Assuming unsuccessful login redirects to '/login'

    def test_my_login_view_authenticated_user_redirect(self):
        url = reverse('login')
        self.client.login(username='user', password='user12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, '/account/', status_code=302, target_status_code=200)
