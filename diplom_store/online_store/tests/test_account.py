from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
from account.models import User

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        person = Person(locale=Locale.RU)
        url = reverse('account-list')
        data = {
            'username': person.username(),
            'first_name': person.first_name(gender=Gender.MALE),
            'last_name': person.last_name(gender=Gender.MALE),
            'surname': person.surname(gender=Gender.MALE),
            'email': person.email(),
            'phone': person.telephone('7##########'),
            'password': '12345',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'DabApps')

