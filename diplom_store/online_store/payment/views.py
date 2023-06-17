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
from payment.services import PaymentService


class PaymentAPIView(APIView):
    """
    Оплата заказа
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSerializer

    def get(self, request, pk, *args, **kwargs):
        print("PK", pk)
        order = Order.objects.filter(orderId=pk).first()
        print("ORDER", order)
        data = {
            "status": order.status
        }
        print("GET_PAYMENT", data)
        return Response(data)

    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(orderId=pk).order_by('-createdAt').first()
        number_of_cart = int("".join(request.data.get('number').split()))
        name = request.data.get('name')
        month = request.data.get('month')
        year = request.data.get('year')
        code = request.data.get('code')

        payment_service = PaymentService()
        payment_service.start_payment_processing(num_workers=2)

        # Обработка платежа
        payment_data = payment_service.process_payment(number_of_cart)
        print("PAYMENT_DATA", payment_data)
        print("PAYMENT_STATUS", payment_data['status'])
        if payment_data['status'] == 'Paid':
            order.status = settings.ORDER_STATUSES[0][1]
            print('Ждём подтверждения оплаты от платёжной системы')
        elif payment_data['status'] == 'Payment error':
            order.status = settings.ORDER_STATUSES[1][1]
            print('Произошла ошибка при оплате. Код ошибки:', payment_data['error_code'])


        # payment_settings = PaymentSettings.objects.first()
        # if order.deliveryType == settings.SHIPPING_METHODS[0][1] and order.totalCost < payment_settings.amount_free:
        #     order.totalCost += payment_settings.standard
        # elif order.deliveryType == settings.SHIPPING_METHODS[1][1]:
        #     order.totalCost += payment_settings.express

        payment = Payment.objects.create(number=str(number_of_cart), name=name, month=month, year=year, code=code)
        order.payment = payment
        order.save()
        print("POST_PAYMENT", order)
        return Response(status=200, template_name="frontend/account.html")

