import logging
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from cart.cart import Cart
from cart.serializers import BasketSerializer
from product.models import Product


logger = logging.getLogger(__name__)


class CartAPIView(APIView):
    """
    Получение продуктов из корзины и их сериализация
    """
    serializer_class = BasketSerializer

    def get(self, request: Request) -> Response:
        """
        Получение продуктов из корзины

        Входные переменные:
            - request: объект запроса
        Возвращаемые значения:
            - response: объект ответа с сериализованными данными продуктов из корзины
        """
        cart = Cart(request)
        products_in_cart = [product for product in cart.cart.keys()]
        products = Product.objects.filter(pk__in=products_in_cart)
        serializer = self.serializer_class(products, many=True, context=cart.cart)
        logger.info(_('Return serializer data cart'))
        return Response(serializer.data)


class BasketAPIView(APIView):
    """
    Представление для получения и удаления продуктов из корзины, добавления продуктов в корзину
    """
    serializer_class = BasketSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        products_in_cart = [product for product in cart.cart.keys()]
        products = Product.objects.filter(pk__in=products_in_cart)
        serializer = self.serializer_class(products, many=True, context=cart.cart)
        logger.info(_('Retrieving products from the cart'))
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
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Добавление продукта в корзину

        Входные переменные:
            - request: объект запроса
        Возвращаемые значения:
            - response: объект ответа с данными добавленного продукта
        """
        id = request.data.get('id')
        count = int(request.data.get('count'))
        cart = Cart(request)

        product = get_object_or_404(Product, pk=id)
        cart.add(
            product=product,
            quantity=count
        )
        serializer = self.serializer_class(product, context=cart.cart)
        logger.info(_('Retrieving products from the cart'))
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
    def delete(self, request, *args, **kwargs) -> Response:
        """
        Удаление продукта из корзины

        Входные переменные:
            - request: объект запроса
        Возвращаемые значения:
            - response: объект ответа с данными удаленного продукта или пустой массив
        """

        cart = Cart(request)
        id = request.data.get('id')
        count = int(request.data.get('count'))
        update_quantity = False

        if cart and cart.cart[str(id)].get('quantity') == count:
            update_quantity = True

        product = get_object_or_404(Product, id=id)
        cart.remove(
            product=product,
            quantity=count,
            update_quantity=update_quantity,
        )
        logger.info(_('Removing products from the shopping cart'))
        if update_quantity:
            return Response(data=[], status=201)
        else:
            # serializer = self.serializer_class(product, context=cart.cart)
            # return Response(data=[serializer.data], status=201)
            products_in_cart = [product for product in cart.cart.keys()]
            products = Product.objects.filter(pk__in=products_in_cart)
            serializer = self.serializer_class(products, many=True, context=cart.cart)
            return Response(data=serializer.data, status=201)
