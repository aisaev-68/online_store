from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from cart.serializers import BasketSerializer
from product.models import Product


def get_products_in_cart(cart):
    """
    Получение продуктов из корзины и их сериализация
    :param cart: корзина продуктов
    :return: сериализованные данные
    """
    products_in_cart = [product for product in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_in_cart)
    serializer = BasketSerializer(products, many=True, context=cart.cart)
    return serializer


class BasketView(View):
    """
    Представление для получения и удаления продуктов из корзины, добавления продуктов в корзину
    """

    def get_success_url(self):
        return reverse_lazy(
            "cart:basket",
        )
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/cart.html', context={'carts': cart})

    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.add(
            product=product,
            quantity=1,
            update_quantity=False,
        )
        return redirect('shopapp:shop_page')

    def delete(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.remove(product)
        url = self.get_success_url()
        return HttpResponseRedirect(url)