from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
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
        print(request.data)
        product_data = request.data # Получаем данные товара из параметра запроса
        context = {
            "orderId": "",
            "createdAt": "",
            "fullName": "",
            "email": "",
            "phone": "",
            "deliveryType": "",
            "paymentType": "",
            "totalCost": 0,
            "status": "",
            "city": "",
            "address": "",
            "products": product_data
        }
        return Response(context)
        # product_serializer = ProductSerializer(data=product_data)
        # if product_serializer.is_valid():
        #     product_instance = product_serializer.save()  # Сохраняем товар и получаем его экземпляр
        #     order_data = {
        #         'products': [product_instance.id],  # Передаем список ID товаров в поле "products"
        #         'totalCost': product_instance.price,  # Устанавливаем общую стоимость заказа
        #         # Добавьте остальные поля заказа, если требуется
        #     }
        #     order_serializer = OrderSerializer(data=order_data)
        #     if order_serializer.is_valid():
        #         order_instance = order_serializer.save()  # Сохраняем заказ
        #         return Response(order_serializer.data, status=201)
        #     else:
        #         product_instance.delete()  # Удаляем сохраненный товар в случае ошибки создания заказа
        #         return Response(order_serializer.errors, status=400)
        # else:
        #     return Response(product_serializer.errors, status=400)



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
