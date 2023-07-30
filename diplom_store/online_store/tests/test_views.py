import random

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from mimesis import Address, Person
from mimesis.enums import Locale, Gender

from shopapp.cart import Cart
from shopapp.forms import OrderModelForm
from shopapp.models import Product, Order, OrderItem, Category


def get_promo_code(num: int):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


class OrderTestCase(TestCase):
    fixtures = [
        'catalog-fixtures.json',
        'category-fixtures.json',
        'groups-fixtures.json',
        'users-fixtures.json',
        'profiles-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        # Запускаются 1 раз перед тестами
        """
        Выборка пользователя и продуктов
        """
        super().setUpClass()

        cls.user = User.objects.get(pk=15)
        cls.products = Product.objects.filter(archived=False)

    def setUp(self) -> None:
        """
        Вход пользователя и создание заказа для дальнейшего теста.
        """

        address = Address(locale=Locale.RU)
        delivery_address = address.country(), address.postal_code(), address.city(), address.address()
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address=delivery_address,
            promocode=get_promo_code(num=20),
            user=self.user,
        )
        for product in self.products[3:6]:
            OrderItem.objects.create(
                order=self.order,
                product=product,
                price=product.price,
                quantity=random.choices([1, 2, 3, 4])[0],
            )

    def tearDown(self) -> None:
        """
        Удаление заказа.
        """
        self.order.delete()

    def test_order_details(self):
        """
        Тест проверяет
         - проверка получения заказа:
         - наличие в теле ответа адреса заказа;
         - наличие в теле ответа промокода;
         - наличие в контексте ответа того же заказа, который был создан;
         - перед тестом (сравнение заказов по первичному ключу).
        """

        response = self.client.get(
            reverse('shopapp:order_detail',
                    args=[self.order.pk]),
        )
        self.assertEqual(response.context['orders'].pk, self.order.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['orders'].delivery_address)
        self.assertTrue(response.context['orders'].promocode)
        self.assertEqual(response.context['orders'], self.order)

    def test_order_create(self):
        self.client.post(
            reverse('shopapp:cart_add', kwargs={"product_id": 1})
        )

        response = self.client.post(
            reverse('shopapp:create_order'), data={
                "delivery_address": "Moscow, str. 23",
                "promocode": "ASD234DS78"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:orders_user", kwargs={"pk": self.user.pk}))

    def test_order_list(self):
        keys = ['image', 'name', 'price', 'count', 'sum', 'created_at', 'delivery_address']
        response = self.client.get(
            reverse('shopapp:orders_user', kwargs={'pk': self.user.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['orders'][0].keys()), keys)
        self.assertTemplateUsed(response, "shopapp/orders-list.html")


class OrdersExportTestCase(TestCase):
    fixtures = [
        'groups-fixtures.json',
        'users-fixtures.json',
        'profiles-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        person = Person(locale=Locale.RU)

        cls.user = User.objects.create_user(
            username=person.username(),
            first_name=person.first_name(gender=Gender.MALE),
            last_name=person.last_name(gender=Gender.MALE),
            email=person.email(),
            password='12345',
            is_staff=True,

        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        pass

    def test_orders_export(self):
        response = self.client.get(
            reverse('shopapp:orders_export')
        )
        orders = Order.objects.select_related("user").prefetch_related("items").all()
        list_orders = []
        for order in orders:
            data = {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "created_at": parse_datetime(str(order.created_at)).strftime('%Y-%m-%d %H:%M:%S'),
                "user": 1,
                "paid": order.paid,
                "products": [{'name': p.product.name,
                              'price': p.price,
                              'quantity': p.quantity,
                              'sum': p.get_sum()}
                             for p in order.items.all()]
            }
            list_orders.append(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['all-orders'])
        self.assertEqual(response.json()['all-orders'], list_orders)


class CartTestCase(TestCase):
    fixtures = [
        'catalog-fixtures.json',
        'category-fixtures.json',
        'groups-fixtures.json',
        'users-fixtures.json',
        'profiles-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        person = Person(locale=Locale.RU)
        cls.user = User.objects.create_user(
            username=person.username(),
            first_name=person.first_name(gender=Gender.MALE),
            last_name=person.last_name(gender=Gender.MALE),
            email=person.email(),
            password='12345',
            is_staff=True,

        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        pass

    def test_cart_add(self):
        response = self.client.post(
            reverse('shopapp:cart_add', kwargs={"product_id": 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:shop_page"))

    def test_cart_update(self):
        response = self.client.post(
            reverse(
                'shopapp:cart_update',
                kwargs={"product_id": 1}
            ),
            data={'quantity': 5, "update": True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:cart_detail"))

    def test_cart_detail(self):
        for i in range(1, 5):
            self.client.post(
                reverse('shopapp:cart_add', kwargs={"product_id": i})
            )

        response = self.client.get(
            reverse('shopapp:cart_detail')
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cart'].cart_count(), 4)
        self.assertTemplateUsed(response, "shopapp/cart.html")

    def test_cart_remove(self):
        res = self.client.post(
            reverse('shopapp:cart_add', kwargs={"product_id": 1})
        )

        response = self.client.post(
            reverse('shopapp:cart_remove', kwargs={"product_id": 1})
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:cart_detail"))


class ProductTestCase(TestCase):
    fixtures = [
        'catalog-fixtures.json',
        'category-fixtures.json',
        'groups-fixtures.json',
        'users-fixtures.json',
        'profiles-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        # Запускаются 1 раз перед тестами
        """
        Выборка продуктов
        """
        super().setUpClass()
        cls.user = User.objects.get(pk=1)
        cls.category = Category.objects.filter(name='Телефоны и смарт часы').first()
        cls.products = Product.objects.filter(archived=False)

    def setUp(self) -> None:
        """
        Вход пользователя и создание заказа для дальнейшего теста.
        """
        self.client.force_login(self.user)


    def tearDown(self) -> None:
        pass

    def test_product_list(self):
        response = self.client.get(
            reverse('shopapp:products_list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


    def test_product_detail(self):
        response = self.client.get(
            reverse('shopapp:product_detail', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopapp/product_detail.html')


    def test_product_create(self):
        response = self.client.post(
            reverse('shopapp:create_product'), data={
                "catalog": self.category.catalog,
                "catalog_eng": self.category,
                "name": "Смартфон Apple iPhone 11 64GB",
                "description": "Смартфон Apple iPhone 11 64 ГБ обладает интересным дизайном и управляется предустановленной операционной системой iOS 14.",
                "attributes": {"Цвет": "Черный"},
                "created_by": 1,
                "rating": 3.2,
                "price": 25090,
                "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcS7JZqEk0p0KALzrLay6wBq2UtBy2agrfsR7C2kP7nnEvtM7f9N&usqp=CAE",
                "discount": 2,
                "sold": 0,
                "products_count": 50,
                "brand": "Apple",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopapp/create_product.html')


    def test_product_archived(self):
        response = self.client.post(
            reverse("shopapp:product_archived", kwargs={"pk": 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:products_list"))

    def tes_product_update(self):
        response = self.client.post(
            reverse("shopapp:update_product", kwargs={"pk": 1}), data={"product_count": 100}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shopapp:product_detail"))