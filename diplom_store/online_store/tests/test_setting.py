from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from settings.models import PaymentSettings
from settings.serializers import PaymentSettingsSerializer
from online_store import settings


class TestSettingsAPIView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.payment_settings = PaymentSettings.objects.create(
            page_size=settings.REST_FRAMEWORK['PAGE_SIZE'],
            express=settings.EXPRESS_SHIPPING_COST,
            standard=settings.STANDARD_SHIPPING_COST,
            amount_free=settings.MIN_AMOUNT_FREE_SHIPPING,
            payment_methods=settings.PAYMENT_METHODS[0][0],
            shipping_methods=settings.SHIPPING_METHODS[0][0],
            order_status=settings.ORDER_STATUSES[0][0],
        )

    def test_get_settings(self):
        # Test getting settings
        url = reverse('settings-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('page_size', response.data)
        self.assertIn('express', response.data)
        self.assertIn('standard', response.data)
        self.assertIn('amount_free', response.data)
        self.assertIn('payment_methods', response.data)
        self.assertIn('shipping_methods', response.data)
        self.assertIn('order_status', response.data)

    def test_update_settings(self):
        # Test updating settings
        url = reverse('settings-list')
        data = {
            'page_size': 50,
            'express': 10,
            'standard': 5,
            'amount_free': 100,
            'payment_methods': 'credit_card',
            'shipping_methods': 'fast',
            'order_status': 'shipped',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page_size'], data['page_size'])
        self.assertEqual(response.data['express'], data['express'])
        self.assertEqual(response.data['standard'], data['standard'])
        self.assertEqual(response.data['amount_free'], data['amount_free'])
        self.assertEqual(response.data['payment_methods'], data['payment_methods'])
        self.assertEqual(response.data['shipping_methods'], data['shipping_methods'])
        self.assertEqual(response.data['order_status'], data['order_status'])