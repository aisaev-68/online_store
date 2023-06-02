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
        product_data = request.data[0]  # Получаем данные товара из параметра запроса
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_instance = product_serializer.save()  # Сохраняем товар и получаем его экземпляр
            order_data = {
                'products': [product_instance.id],  # Передаем список ID товаров в поле "products"
                'totalCost': product_instance.price,  # Устанавливаем общую стоимость заказа
                # Добавьте остальные поля заказа, если требуется
            }
            order_serializer = OrderSerializer(data=order_data)
            if order_serializer.is_valid():
                order_instance = order_serializer.save()  # Сохраняем заказ
                return Response(order_serializer.data, status=201)
            else:
                product_instance.delete()  # Удаляем сохраненный товар в случае ошибки создания заказа
                return Response(order_serializer.errors, status=400)
        else:
            return Response(product_serializer.errors, status=400)



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


class OrdersView(viewsets.ModelViewSet):
    """
    Представление для получения, сохранения данных по заказам
    """
    queryset = Order.objects.all().select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer

    def submit_basket(self, request, *args, **kwargs):
        if request.user.pk:
            user = User.objects.get(pk=request.user.pk)
            fullName, email, phone = user.fullName, user.email, user.phone
        else:
            user = request.user
            fullName, email, phone = '', '', ''
        products = request.data
        totalCost = sum([product.get('count') * product.get('price') for product in products])
        data_of_order = {'user': user,
                         'products': products,
                         'fullName': fullName,
                         'email': email,
                         'phone': phone,
                         'totalCost': totalCost,
                         }
        serializer = self.get_serializer(data=data_of_order)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def active(self, request):
        order = self.queryset.last()
        cart = Cart(request).cart

        if cart:
            for product in order.products.all():
                product.count = cart.get(str(product.pk)).get('count')
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart = Cart(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        for product in instance.products.all():
            product.count -= cart.cart.get(str(product.pk)).get('count')
            if product.count <= 0:
                product.active = False
            product.save()
        cart.clear()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user_id=request.user.pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'orders': serializer.data})

    def details(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)
