from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product
from cart.cart import Cart
from cart.serializers import BasketSerializer


class TestCartAPIView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product1 = Product.objects.create(title='Product 1', price=100, available=True)
        self.product2 = Product.objects.create(title='Product 2', price=200, available=True)

        self.cart = Cart(self.client.session)
        self.cart.add(product=self.product1, quantity=2)
        self.cart.add(product=self.product2, quantity=1)

    def test_get_cart_items(self):
        # Test getting products from the cart
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)

    def test_add_to_cart(self):
        # Test adding a product to the cart
        url = reverse('basket-list')
        data = {'id': self.product1.id, 'count': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data[0])
        self.assertIn('count', response.data[0])

    def test_delete_from_cart(self):
        # Test removing a product from the cart
        url = reverse('basket-list')
        data = {'id': self.product2.id, 'count': 1}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [])

        # Test removing the last quantity of a product from the cart
        data = {'id': self.product1.id, 'count': 2}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [])

        # Test removing a non-existent product from the cart
        data = {'id': 999, 'count': 1}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [])