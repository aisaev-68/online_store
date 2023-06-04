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
    # authentication_classes = (SessionAuthentication,)

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


# class CartDetail(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         cart = Cart(request)
#         form = OrderModelForm()
#         for item in cart:
#             item['update_quantity_form'] = CartAddProductForm(
#                 initial={'quantity': item['quantity'],
#                          'update': True})
#
#         return render(request, 'shopapp/cart.html', context={'cart': cart, 'form': form})
#
#
# class CartAdd(LoginRequiredMixin, View):
#
#     def post(self, request: HttpRequest, product_id):
#         cart = Cart(request)
#         product = get_object_or_404(Product, pk=product_id)
#         cart.add(
#                 product=product,
#                 quantity=1,
#                 update_quantity=False,
#             )
#         return redirect('shopapp:shop_page')
#
#
# class CartDelete(LoginRequiredMixin, View):
#     def get_success_url(self):
#         return reverse_lazy(
#             "shopapp:cart_detail",
#         )
#
#     def post(self, request, *args, **kwargs):
#         cart = Cart(request)
#         product = get_object_or_404(Product, id=self.kwargs['product_id'])
#         cart.remove(product)
#         url = self.get_success_url()
#         return HttpResponseRedirect(url)
#
#
# class CartUpdate(LoginRequiredMixin, View):
#
#     def post(self, request, product_id):
#         cart = Cart(request)
#         product = get_object_or_404(Product, pk=product_id)
#         form = CartAddProductForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             dif_count = product.products_count - cd['quantity']
#             if dif_count >= 0:
#                 cart.add(
#                     product=product,
#                     quantity=cd['quantity'],
#                     update_quantity=cd['update'],
#                 )
#         return redirect('shopapp:cart_detail')
#
#         # return render(request, 'shopapp/cart.html', context={'cart': cart, 'form': form, 'message': f'Only {product.products_count} products left.'})
