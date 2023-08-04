from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from account.models import User
from product.models import Product, Manufacturer, Seller
from cart.cart import Cart
from catalog.models import Category

from cart.serializers import BasketSerializer


class TestCartAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('cart:cart')
        self.user = self.user = User.objects.create_user(
            username='user',
            email='user@user.ru',
            password='user12345',
            phone="89305484111",
            last_name="Иванов",
            first_name="Иван",
            surname="Иванович"
        )
        self.client.login(username='user', password='user12345')

        self.category = Category.objects.create(
                title='Laptop',
                src='/catalog/1.png',
            )
        self.seller = Seller.objects.create(
            name='Ozon',
            city='Moscow',
            address='str. 1',
        )
        self.brand = Manufacturer.objects.create(name='Apple')
        self.product1 = Product.objects.create(
            category=self.category,
            title='Product 1',
            fullDescription="Product 1 bla-bla-bla",
            attributes={},
            price=20000.0,
            count=50,
            brand=self.brand,
            seller=self.seller,
            banner=True,
            available=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            title='Product 2',
            fullDescription="Product 2 bla-bla-bla",
            attributes={},
            price=10000.0,
            count=10,
            brand=self.brand,
            seller=self.seller,
            banner=True,
            available=True
        )

        self.cart = Cart(self.client.session)
        self.cart.add(product=self.product1, quantity=2)
        self.cart.add(product=self.product2, quantity=1)

    def tearDown(self):
        self.user.delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Seller.objects.all().delete()
        Manufacturer.objects.all().delete()

    def test_get_cart_items(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)

    # def test_add_to_cart(self):
    #
    #     data = {'id': self.product1.id, 'count': 1}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('id', response.data[0])
    #     self.assertIn('count', response.data[0])
    #
    # def test_delete_from_cart(self):
    #
    #     data = {'id': self.product2.id, 'count': 1}
    #     response = self.client.delete(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data, [])
    #
    #     data = {'id': self.product1.id, 'count': 2}
    #     response = self.client.delete(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data, [])
    #
    #     data = {'id': 999, 'count': 1}
    #     response = self.client.delete(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data, [])