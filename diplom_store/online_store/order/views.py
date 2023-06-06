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
from order.models import Order, OrderProducts
from order.serializers import OrderSerializer, OrderProductSerializer

from product.serializers import ProductSerializer, ProductOrderSerializer


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
        responses={201: OrderProductSerializer}
    )
    def post(self, request):
        products_data = request.data  # Получаем данные о продуктах из запроса

        order = Order.objects.create(user=request.user)
        for product_data in products_data:
            order_product = OrderProducts()
            order_product.order = order
            order_product.product_id = product_data['id']
            order_product.count_in_order = product_data['count']
            # Задайте остальные поля
            order_product.save()

        serializer = OrderProductSerializer(instance=order)
        print("SER", serializer.data)

        # # Очистка корзины в сессии
        # request.session.pop('cart')


        return Response(serializer.data, status=201)

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
        order = Order.objects.filter(status='В процессе').first()
        print("ORDER", order)
        cart = Cart(request).cart
        serializer = OrderProductSerializer(order)
        return Response(serializer.data)
