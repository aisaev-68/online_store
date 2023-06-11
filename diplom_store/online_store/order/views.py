from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from account.forms import LoginForm
from account.models import User
from cart.cart import Cart
from order.models import Order, OrderProducts
from order.serializers import OrderSerializer, OrderProductSerializer

from product.serializers import ProductSerializer, ProductOrderSerializer


class OrderView(APIView):
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = self.serializer_class(orders, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: OrderProductSerializer}
    )

    def post(self, request):
        if request.user.is_authenticated:
            order_products = []
            total = 0
            user = request.user
            products_data = request.data  # Получаем данные о продуктах из запроса

            order = Order.objects.create(user=user)
            for product_data in products_data:
                order_product = OrderProducts()
                order_product.order = order
                order_product.product_id = product_data['id']
                order_product.count_product = product_data['count']
                total += product_data['count'] * product_data['price']
                # Задайте остальные поля
                order_product.save()
            order.totalCost = total
            order.user = request.user
            order.save()

            orders = OrderProductSerializer(instance=order).data

            return Response([orders], status=201)
        else:
            # return Response({"detail": "Authentication required."}, status=401)
            return render(request, 'account/login.html', context={"form": LoginForm()})




class OrderByIdView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderSerializer

    def get(self, pk, request, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        serializer = self.serializer_class(order)
        print('ORDER_ID', serializer.data)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        order.fullName = request.data.get('fullName')
        order.phone = request.data.get('phone')
        order.email = request.data.get('email')
        order.delivery_type = request.data.get('deliveryType')
        order.city = request.data.get('city')
        order.address = request.data.get('address')
        order.payment_type = request.data.get('paymentType')
        order.save()

        return Response(status=200)


class OrderActiveView(APIView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(status=_('In progress')).order_by('-createdAt').first()

        cart = Cart(request).cart
        serializer = OrderProductSerializer(order)
        print("ORDER_ACTIVE", serializer.data)
        return Response(serializer.data)
