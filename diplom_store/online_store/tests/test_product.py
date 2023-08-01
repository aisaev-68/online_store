from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from order.models import Order
from payment.models import Payment
from payment.serializers import PaymentSerializer


class TestPaymentAPIView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.order = Order.objects.create(
            user=self.user,
            status='status_value',
            orderId='order_id_value',
        )

        self.payment = Payment.objects.create(
            number='1234567890',
            name='John Doe',
            month='12',
            year='2025',
            code='123',
        )
        self.order.payment = self.payment
        self.order.save()

    def test_get_payment_status(self):
        # Test getting payment status for an order
        url = reverse('payment-status')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('orderId', response.data)

    def test_post_payment(self):
        # Test posting payment data for an order
        url = reverse('payment-status')
        data = {
            'number': '1234 5678 9012 3456',
            'name': 'John Doe',
            'month': '12',
            'year': '2025',
            'code': '123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.template_name[0], 'frontend/account.html')
        self.assertTrue(Order.objects.filter(status='status_value', payment__number='1234567890123456').exists())
        self.assertTrue(Payment.objects.filter(number='1234567890123456').exists())