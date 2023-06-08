from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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
        print(3333, serializer.data)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: OrderProductSerializer}
    )

    def post(self, request):
        if request.user.is_authenticated:
            order_products = []
            user = request.user
            products_data = request.data  # Получаем данные о продуктах из запроса
            print("PRODUCTS_DATA", products_data)
            order = Order.objects.create(user=user)
            for product_data in products_data:
                order_product = OrderProducts()
                order_product.order = order
                order_product.product_id = product_data['id']
                order_product.count_in_order = product_data['count']
                # Задайте остальные поля
                order_product.save()

                # product_dict = {
                #     'id': product_data['id'],
                #     'category': product_data['category'],
                #     'price': product_data['price'],
                #     'count': product_data['count'],
                #     'date': product_data['date'],
                #     'title': product_data['title'],
                #     'description': product_data['description'],
                #     'href': product_data['href'],
                #     'freeDelivery': product_data['freeDelivery'],
                #     'images': [{'image': image} for image in product_data['images']],
                #     'tags': product_data['tags'],
                #     'reviews': product_data['reviews'],
                #     'rating': product_data['rating']
                # }
                # order_products.append(product_dict)


            orders = OrderProductSerializer(instance=order).data
            orders['products'] = products_data
            print("SER", orders)

            return Response(orders, status=201)
        else:
            # return Response({"detail": "Authentication required."}, status=401)
            return render(request, 'account/login.html', context={"form": LoginForm()})




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
