from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from online_store import settings
from order.models import Order

from payment.models import Payment, PaymentSettings

from payment.serializers import PaymentSerializer



class PaymentAPIView(APIView):
    """
    Оплата заказа
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSerializer

    def post(self, request, pk, *args, **kwargs):
        print("PAYMENT", request.data)
        order = Order.objects.filter(orderId=pk).order_by('-createdAt').first()
        number_of_cart = int("".join(request.data.get('number').split()))
        name = request.data.get('name')
        month = request.data.get('month')
        year = request.data.get('year')
        code = request.data.get('code')
        print(222, settings.ORDER_STATUSES[1])
        if number_of_cart % 2 == 0 and number_of_cart % 10 != 0:
            order.status = settings.ORDER_STATUSES[1][0]
        else:
            order.status = settings.ORDER_STATUSES[2][0]

        payment_settings = PaymentSettings.objects.first()
        if order.deliveryType == settings.SHIPPING_METHODS[0][0] and order.totalCost < payment_settings.amount_free:
            order.totalCost += payment_settings.standard
        elif order.deliveryType == settings.SHIPPING_METHODS[1][0]:
            order.totalCost += payment_settings.express

        payment = Payment.objects.create(number=str(number_of_cart), name=name, month=month, year=year, code=code)
        order.payment = payment
        order.save()

        return Response(status=200)

