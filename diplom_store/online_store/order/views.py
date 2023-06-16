from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
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

from online_store import settings

from payment.models import PaymentSettings


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderProductSerializer

    def pagination_queryset(self):

        paginator = PageNumberPagination()
        payment_settings = PaymentSettings.objects.first()
        limit = payment_settings.page_size

        paginator.page_size = limit
        queryset = Order.objects.all()
        len_orders = len(queryset)

        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        current_page = int(self.request.GET.get('page', 1))
        if len_orders % limit == 0:
            last_page = len_orders // limit
        else:
            last_page = len_orders // limit + 1

        return {
            'pagination': serializer.data,
            'currentPage': current_page,
            'lastPage': last_page,
        }
    def get(self, request, *args, **kwargs):
        # queryset = Order.objects.all()
        data = self.pagination_queryset()
        # paginated_queryset = data['pagination']
        # serializer = self.serializer_class(paginated_queryset, many=True)
        print("HISTORY ORDERS", data)
        return Response(data)

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
            order.fullName = user.fullName
            order.phone = user.phone
            order.email = user.email
            order.totalCost = total
            order.user = request.user
            order.save()

            orders = OrderProductSerializer(instance=order).data

            return Response([orders], status=201)
        else:
            # return Response({"detail": "Authentication required."}, status=401)
            return render(request, 'account/login.html', context={"form": LoginForm()})




class ConfirmOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderProductSerializer

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        serializer = self.serializer_class(order)
        print('ORDER_ID', serializer.data)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        payment_settings = PaymentSettings.objects.first()
        order = Order.objects.get(pk=pk)
        order.fullName = request.data.get('fullName')
        order.phone = request.data.get('phone')
        order.email = request.data.get('email')
        order.deliveryType = request.data.get('deliveryType')
        order.city = request.data.get('city')
        order.address = request.data.get('address')
        order.paymentType = request.data.get('paymentType')
        order.totalCost = request.data.get('totalCost')

        # Добавить стоимость доставки экспресс-доставки
        if order.deliveryType == settings.SHIPPING_METHODS[0][0]:
            order.totalCost += payment_settings.express
        else:
            # Добавить стоимость обычной доставки
            if order.totalCost < payment_settings.amount_free:
                order.totalCost += payment_settings.standard

        order.save()
        print("ORDER SUCCESS",  OrderProductSerializer(order).data)
        return Response(status=200)



class OrderActiveAPIView(APIView):

    def get(self, request, *args, **kwargs):
        print(44444, self.request, self.kwargs, args, kwargs, request.data)
        order = Order.objects.filter(status='pending_payment').first()

        cart = Cart(request).cart
        serializer = OrderProductSerializer(order)
        print("ORDER_ACTIVE", serializer.data)
        return Response(serializer.data)
