from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.urls import reverse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
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
        # print("BASKET_GET", serializer.data)
        return Response(data=serializer.data, status=200)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['id', 'count'],
        ),
        # responses={
        #     201: openapi.Schema(
        #         type=openapi.TYPE_ARRAY,
        #         items=openapi.Schema(
        #             type=openapi.TYPE_OBJECT,
        #             properties=BasketSerializer().fields,
        #         ),
        #     ),
        # }
    )
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        count = request.data.get('count')
        cart = Cart(request)
        product = get_object_or_404(Product, pk=id)
        cart.add(
            product=product,
            quantity=count
        )
        serializer = self.serializer_class(product, context=cart.cart)
        # print("BASKET_POST", serializer.data)
        return Response(data=[serializer.data], status=201)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['id', 'count'],
        ),
        # responses={
        #     201: openapi.Schema(
        #         type=openapi.TYPE_ARRAY,
        #         items=openapi.Schema(
        #             type=openapi.TYPE_OBJECT,
        #             properties=BasketSerializer().fields,
        #         ),
        #     ),
        # }
    )
    def delete(self, request, *args, **kwargs):
        # print("DATA", request.data)
        cart = Cart(request)
        id = request.data.get('id')
        count = request.data.get('count')
        update_quantity = False
        print("COUNT_DELETE_VIEW", id, cart.cart[str(id)])
        #cart.cart[str(id)].get('quantity') == 1 or
        if cart.cart[str(id)].get('quantity') == count:
            update_quantity = True

        product = get_object_or_404(Product, id=id)
        cart.remove(
            product=product,
            quantity=count,
            update_quantity=update_quantity,
        )
        print("CART", cart.cart, update_quantity)


        if update_quantity:
            return Response(data=[], status=201)
        else:
            serializer = self.serializer_class(product, context=cart.cart)
            return Response(data=[serializer.data], status=201)

        # if cart.cart:
        #     return HttpResponseRedirect(reverse('index'))
        print("ser_data", serializer.data)


