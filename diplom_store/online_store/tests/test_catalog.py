from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from catalog.models import Category
from product.models import Product


class TestCatalogAPI(APITestCase):

    def setUp(self):
        # Create some test data for the Category and Product models
        self.category = Category.objects.create(title='Планшеты')
        self.product1 = Product.objects.create(title='Product 1', category=self.category, price=100, available=True)
        self.product2 = Product.objects.create(title='Product 2', category=self.category, price=200, available=True)

    def test_get_categories(self):
        # Test getting product categories
        url = reverse('category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming there is only one category in the test data

    def test_get_catalog_items(self):
        # Test filtering and pagination of catalog items
        url = reverse('catalog')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)

    def test_get_popular_products(self):
        # Test getting popular products
        url = reverse('popular-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)

    def test_get_limited_products(self):
        # Test getting limited products
        url = reverse('limited-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)

    def test_get_sales_products(self):
        # Test getting products with sales
        url = reverse('sales-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('salesCards', response.data)
        self.assertIn('currentPage', response.data)
        self.assertIn('lastPage', response.data)

    def test_get_banners(self):
        # Test getting banners
        url = reverse('banners-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)

    def test_search_products(self):
        # Test searching for products
        search_text = 'Product'
        url = reverse('search-list')
        response = self.client.get(url, {'filterSearch': search_text})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category', response.data)