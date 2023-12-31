import logging
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from cart.cart import Cart
from order.models import Order, OrderProducts
from order.serializers import OrderSerializer, OrderProductSerializer

from product.serializers import ProductSerializer, ProductOrderSerializer

from online_store import settings

from settings.models import PaymentSettings

logger = logging.getLogger(__name__)


class OrderHistoryAPiView(APIView):
    """
    Представление для получения истории заказов.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = OrderProductSerializer

    def pagination_queryset(self):

        paginator = PageNumberPagination()
        payment_settings = PaymentSettings.objects.first()

        if payment_settings:
            limit = payment_settings.page_size
        else:
            limit = settings.REST_FRAMEWORK['PAGE_SIZE']

        paginator.page_size = limit
        queryset = Order.objects.filter(user=self.request.user).order_by('-createdAt').all()
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
        data = self.pagination_queryset()
        logger.info(_('Getting order history'))
        return Response(data, status=200)

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
            print(products_data)
            order = Order.objects.create(user=user)
            for product_data in products_data:
                order_product = OrderProducts()
                order_product.order = order
                order_product.product_id = product_data['id']
                order_product.count_product = product_data['count']
                total += product_data['count'] * product_data['price']
                order_product.save()
            order.fullName = user.fullName
            order.phone = user.phone
            order.email = user.email
            order.totalCost = total
            order.user = request.user
            order.save()

            Cart(request).clear()

            orders = OrderProductSerializer(instance=order).data
            logger.info(_('Saving an order'))
            return Response([orders], status=201)
        else:
            logger.info(_('You must be logged in to view orders'))
            return HttpResponseRedirect(reverse('login'))


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = OrderProductSerializer

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(user=request.user, orderId=pk)
        serializer = self.serializer_class(order)
        logger.info(_('Getting an order by ID'))
        return Response(serializer.data, status=200)

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
        if order.deliveryType == settings.SHIPPING_METHODS[0][1]:
            order.totalCost += payment_settings.express
        else:
            # Добавить стоимость обычной доставки
            if order.totalCost < payment_settings.amount_free:
                order.totalCost += payment_settings.standard

        order.save()

        serializer = self.serializer_class(order)
        logger.info(_('Saving an order by ID'))
        return Response(serializer.data, status=201)


class OrderActiveAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = OrderProductSerializer

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, status=2)
        serializer = self.serializer_class(order)
        logger.info(_('Getting an active order № %s'), order.orderId)

        return Response(serializer.data, status=200)
