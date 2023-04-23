from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from order.models import Order
from order.serializers import OrderSerializer


class OrderView(View):
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user_id=request.user.pk)
        page = Paginator(queryset)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(queryset, many=True)
        return Response({'orders': serializer.data})

    def post(self, request, *args, **kwargs):
        pass


class OrderByIdView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pass


class OrderActiveView(APIView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.all().select_related('user').prefetch_related('products').last()
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
            user = Profile.objects.get(pk=request.user.pk)
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