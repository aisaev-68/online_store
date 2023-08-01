from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from order.models import Order, OrderProducts
from order.serializers import OrderProductSerializer
from product.models import Product


class TestOrderAPViews(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(title='Test Product', price=100, available=True)

        self.order = Order.objects.create(
            user=self.user,
            fullName='John Doe',
            phone='123456789',
            email='john@example.com',
            totalCost=100,
        )

        self.order_product = OrderProducts.objects.create(
            order=self.order,
            product=self.product,
            count_product=2
        )

    def test_get_order_history(self):
        # Test getting order history
        url = reverse('order-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pagination', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)

    def test_create_order(self):
        # Test creating an order
        url = reverse('order-history')
        data = [{'id': self.product.id, 'count': 3, 'price': self.product.price}]
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('fullName', response.data[0])
        self.assertIn('phone', response.data[0])
        self.assertIn('email', response.data[0])
        self.assertIn('totalCost', response.data[0])
        self.assertIn('products', response.data[0])

    def test_get_order_by_id(self):
        # Test getting an order by ID
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fullName', response.data)
        self.assertIn('phone', response.data)
        self.assertIn('email', response.data)
        self.assertIn('totalCost', response.data)
        self.assertIn('products', response.data)

    def test_update_order_by_id(self):
        # Test updating an order by ID
        url = reverse('order-detail', args=[self.order.id])
        data = {
            'fullName': 'Updated Name',
            'phone': '987654321',
            'email': 'updated@example.com',
            'deliveryType': 'express',
            'city': 'New City',
            'address': 'New Address',
            'paymentType': 'credit_card',
            'totalCost': 150,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['fullName'], data['fullName'])
        self.assertEqual(response.data['phone'], data['phone'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['totalCost'], data['totalCost'])

    def test_get_active_order(self):
        # Test getting an active order
        url = reverse('order-active')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fullName', response.data)
        self.assertIn('phone', response.data)
        self.assertIn('email', response.data)
        self.assertIn('totalCost', response.data)
        self.assertIn('products', response.data)