from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from account.models import User
from cart.cart import Cart
from order.models import Order
from order.serializers import OrderSerializer

from product.serializers import ProductSerializer


class OrderView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = self.serializer_class(orders, many=True)
        print(3333, serializer.data)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: OrderSerializer}
    )
    def post(self, request):
        products_data = request.data  # Получаем данные о продуктах из запроса
        print("PRODUCTS", products_data)
        serializer = self.serializer_class(data={"products": request.data})  # Создаем экземпляр сериализатора с полученными данными
        #print(1111111, serializer.data)
        if serializer.is_valid(raise_exception=True):
            print(111, serializer.data)
            # Действия с сериализованными данными
        else:
            print(2222, serializer.errors)
        # if serializer.is_valid(raise_exception=True):
        #     products = serializer.validated_data.get('products', [])  # Извлекаем данные о продуктах
        #     print("PRODUCTS", products)
        #     if not products:
        #         raise ValidationError('No products provided.')

        # Дополнительные проверки и обработка продуктов
        # ...

        # Создание заказа и сохранение данных
        # order = Order.objects.create()
        # order.products.set(products)
        #
        # # Очистка корзины в сессии
        # request.session.pop('cart')

        # Возвращаем успешный ответ с данными о заказе
        response_data = {
            "orderId": "123",
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
                {
                    "id": "123",
                    "category": "55",
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "href": "/catalog/123",
                    "freeDelivery": True,
                    "images": [
                        "string"
                    ],
                    "tags": [
                        "string"
                    ],
                    "reviews": 5,
                    "rating": 4.6
                }
            ]
        }
        return Response(response_data, status=201)

    # return Response(status=400)


class OrderByIdView(View):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderSerializer

    def get(self, pk, request, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        serializer = self.serializer_class(order)
        print('ORDER_ID', serializer.data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pass


class OrderActiveView(APIView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        print("ORDER", order)
        cart = Cart(request).cart

        if cart:
            for product in order.products.all():
                product.count = cart.get(str(product.pk)).get('count')
        serializer = OrderSerializer(order)
        return Response(serializer.data)
