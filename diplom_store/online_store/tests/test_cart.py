import json

from rest_framework.test import APITestCase
from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from account.models import User
from product.models import Product, Manufacturer, Seller
from catalog.models import Category
from tag.models import Tag
from order.models import Order
from cart.cart import Cart
from settings.models import PaymentSettings
from online_store import settings


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class TestAllView(TestCase):
    fixtures = [
        'groups-fixtures.json',
        'users-fixtures.json',
        'catalog-fixtures.json',
        'tag-fixtures.json',
        'settings-fixtures.json',
        'product-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        # Запускаются 1 раз перед тестами
        """
        Выборка пользователя и продуктов
        """
        super().setUpClass()

        cls.user = User.objects.get(
            username='admin'
        )
        cls.product1 = Product.objects.get(id=1)

    def setUp(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.payment_settings = PaymentSettings.objects.create(
            page_size=settings.REST_FRAMEWORK['PAGE_SIZE'],
            express=settings.EXPRESS_SHIPPING_COST,
            standard=settings.STANDARD_SHIPPING_COST,
            amount_free=settings.MIN_AMOUNT_FREE_SHIPPING,
            payment_methods=settings.PAYMENT_METHODS[0][0],
            shipping_methods=settings.SHIPPING_METHODS[0][0],
            order_status=settings.ORDER_STATUSES[0][0],
        )


    def tearDown(self):
        Group.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Seller.objects.all().delete()
        Manufacturer.objects.all().delete()
        Tag.objects.all().delete()
        Order.objects.all().delete()
        PaymentSettings.objects.all().delete()

    def test_my_login_view_valid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': '12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/api/account/')  # Assuming successful login redirects to '/profile'

    def test_my_login_view_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': '123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login/')  # Assuming unsuccessful login redirects to '/login'

    def test_my_login_view_authenticated_user_redirect(self):
        url = reverse('login')
        self.client.login(username='admin', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_settings(self):
        # Test getting settings
        url = reverse('settings:settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('page_size', response.data)
        self.assertIn('express', response.data)
        self.assertIn('standard', response.data)
        self.assertIn('amount_free', response.data)
        self.assertIn('payment_methods', response.data)
        self.assertIn('shipping_methods', response.data)
        self.assertIn('order_status', response.data)

    # Not work: Forbidden: /api/settings/
    def test_update_settings(self):
        # Test updating settings
        user = User.objects.get(username='superuser')
        # self.client.login(username=user.username, password=user.password)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        url = reverse('settings:settings')
        data = {
            'page_size': 6,
            'express': 1000.00,
            'standard': 500.000,
            'amount_free': 1000.00,
            'payment_methods': 1,
            'shipping_methods': 1,
            'order_status': 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page_size'], data['page_size'])
        self.assertEqual(Decimal(response.data['express']), Decimal(data['express']))
        self.assertEqual(Decimal(response.data['standard']), Decimal(data['standard']))
        self.assertEqual(Decimal(response.data['amount_free']), Decimal(data['amount_free']))
        self.assertEqual(response.data['payment_methods'], data['payment_methods'])
        self.assertEqual(response.data['shipping_methods'], data['shipping_methods'])
        self.assertEqual(response.data['order_status'], data['order_status'])


    def test_add_to_cart(self):
        self.url = reverse('cart:basket')
        data = {'id': self.product1.id, 'count': 3}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data[0])
        self.assertIn('count', response.data[0])


    def test_get_cart_items(self):
        self.url = reverse('cart:basket')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('count', response.data)

    def test_delete_from_cart(self):
        self.url = reverse('cart:basket')
        data = {'id': self.product1.id, 'count': 1}
        response = self.client.delete(path=self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [])


    def test_get_categories(self):
        # Test getting product categories
        url = reverse('catalog:category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)  # Assuming there is only one category in the test data

    def test_get_catalog_items(self):
        # Test filtering and pagination of catalog items
        url = reverse('catalog:catalog')
        response = self.client.get(url, {'category': 19})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)

    def test_get_popular_products(self):
        # Test getting popular products
        url = reverse('catalog:product_popular')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])

    def test_get_limited_products(self):
        # Test getting limited products
        url = reverse('catalog:product_limited')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])

    def test_get_sales_products(self):
        # Test getting products with sales
        url = reverse('catalog:sales')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('salesCards', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)

    def test_get_banners(self):
        # Test getting banners
        url = reverse('catalog:banners')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])

    def test_search_products(self):
        # Test searching for products
        search_text = 'Lenovo'
        url = reverse('catalog:search')
        response = self.client.get(url, {'filterSearch': search_text})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category', response.data)


    def test_get_tags(self):
        # Test getting all tags
        url = reverse('tag:tags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data[0])


    def test_create_order(self):
        # Test creating an order
        user = User.objects.get(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse('order:history-order')
        self.product = Product.objects.get(id=2)
        data = [{'id': self.product.id, 'count': 3, 'price': self.product.price}]
        response = self.client.post(url, json.dumps(data, cls=DecimalEncoder), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('fullName', response.data[0])
        self.assertIn('phone', response.data[0])
        self.assertIn('email', response.data[0])
        self.assertIn('totalCost', response.data[0])
        self.assertIn('products', response.data[0])

    def test_get_order_history(self):
        # Test getting order history
        user = User.objects.get(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse('order:history-order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pagination', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)


    def test_get_order_by_id(self):
        # Test getting an order by ID
        user = User.objects.get(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse('order:history-order')
        self.product = Product.objects.get(id=3)
        data = [{'id': self.product.id, 'count': 3, 'price': self.product.price}]
        response = self.client.post(url, json.dumps(data, cls=DecimalEncoder), content_type='application/json')
        url = reverse('order:order', args=[response.data[0].get('orderId')])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fullName', response.data)
        self.assertIn('phone', response.data)
        self.assertIn('email', response.data)
        self.assertIn('totalCost', response.data)
        self.assertIn('products', response.data)


    def test_get_active_order(self):
        # Test getting an active order
        user = User.objects.get(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        Order.objects.create(user=user, status=2)
        url = reverse('order:active-order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fullName', response.data)
        self.assertIn('phone', response.data)
        self.assertIn('email', response.data)
        self.assertIn('totalCost', response.data)
        self.assertIn('products', response.data)

    # def test_update_order_by_id(self):
    #     # Test updating an order by ID
    #     user = User.objects.get(username='admin')
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=user)
    #     order = Order.objects.create(user=user, status=2)
    #     url = reverse('order:order', args=[order.orderId])
    #     data = {
    #         'fullName': 'Updated Name',
    #         'phone': '8987654321',
    #         'email': 'updated@example.com',
    #         'deliveryType': 'express',
    #         'city': 'New City',
    #         'address': 'New Address',
    #         'paymentType': 'credit_card',
    #         'totalCost': 150,
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['fullName'], data['fullName'])
    #     self.assertEqual(response.data['phone'], data['phone'])
    #     self.assertEqual(response.data['email'], data['email'])
        # self.assertEqual(response.data['totalCost'], data['totalCost'])