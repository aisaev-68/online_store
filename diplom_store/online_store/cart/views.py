from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from cart.cart import Cart
from cart.serializers import BasketSerializer
from product.models import Product

from product.serializers import ProductSerializer


class CartAPIView(APIView):
    """
    Получение продуктов из корзины и их сериализация
    :param cart: корзина продуктов
    :return: сериализованные данные
    """

    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    serializer_class = BasketSerializer
    def get(self, request):
        cart = Cart(request)
        products_in_cart = [product for product in cart.cart.keys()]
        print(111111, products_in_cart)
        products = Product.objects.filter(pk__in=products_in_cart)
        serializer = self.serializer_class(products, many=True, context=cart.cart)
        return Response(serializer.data)





class BasketAPIView(APIView):
    """
    Представление для получения и удаления продуктов из корзины, добавления продуктов в корзину
    """
    serializer_class = BasketSerializer
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        products_in_cart = [product for product in cart.cart.keys()]
        products = Product.objects.filter(pk__in=products_in_cart)
        serializer = self.serializer_class(products, many=True, context=cart.cart)
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        count = request.data.get('count', 1)
        cart = Cart(request)
        product = get_object_or_404(Product, pk=id)
        cart.add(
            product=product,
            quantity=count,
            update_quantity=False,
        )
        serializer = self.serializer_class(product, context=cart.cart)
        print(1234, serializer.data)
        return Response(data=serializer.data, status=201)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        count = request.data.get('count', 1)
        update_quantity = request.data.get('remove')
        print(3333, id, count, update_quantity)
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        cart.remove(
            product=product,
            update_quantity=update_quantity
        )
        print('context', cart.cart)
        if update_quantity:
            serializer = ProductSerializer(product)
        else:
            serializer = self.serializer_class(product, context=cart.cart)
        return Response(data=serializer.data, status=201)

