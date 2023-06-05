from decimal import Decimal

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
from order.serializers import OrderSerializer, OrderActiveSerializer

from product.serializers import ProductSerializer




class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
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
        print(request.data)
        carts = Cart(request).cart # list(cart.keys() index
        products_data = request.data  # Получаем данные товара из параметра запроса
        order = Order.objects.create()
        # product_ids = [product_data['id'] for product_data in products_data]
        # products = Product.objects.filter(id__in=product_ids)
        total_cost = 0
        for key, value in carts.items():
            OrderProducts.objects.create(order_id=order.id, product_id=key, count_in_order=value['quantity'])
            total_cost += Decimal(value['quantity']) * Decimal(value['price'])
        order.totalCost = total_cost
        order.save()
        context = {
            "orderId": order.pk,
            "createdAt": order.createdAt.strftime('%Y-%m-%d %H:%M'),
            "fullName": request.user.fullName if not request.user.is_anonymous else "",
            "email": order.user.email if request.user.is_anonymous else "",
            "phone": order.user.phone if request.user.is_anonymous else "",
            "deliveryType": order.deliveryType,
            "paymentType": order.paymentType,
            "totalCost": order.totalCost,
            "status": order.status,
            "city": order.city if order.city else "",
            "address": order.address if order.address else "",
            "products": products_data
        }
        return Response(context)

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
        print("ORDER_ACTIVE", Cart(request).cart)
        serialize = OrderActiveSerializer(data=order)
        if serialize.is_valid():
            print("REQUEST_SESSION", serialize.data)
        else:
            print('ERROR')
        # serializer = OrderSerializer(order)

        context = {
            "orderId": order.pk,
            "createdAt": order.createdAt.strftime('%Y-%m-%d %H:%M'),
            "fullName": request.user.fullName if not request.user.is_anonymous else "",
            "email": order.user.email if request.user.is_anonymous else "",
            "phone": order.user.phone if request.user.is_anonymous else "",
            "deliveryType": order.deliveryType,
            "paymentType": order.paymentType,
            "totalCost": order.totalCost,
            "status": order.status,
            "city": order.city if order.city else "",
            "address": order.address if order.address else "",
            "products": serialize.data
        }
        return Response(context)
