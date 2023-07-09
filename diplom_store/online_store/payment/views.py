from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from rest_framework.response import Response

from order.models import Order
from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.services import PaymentService
from online_store import settings


class PaymentAPIView(APIView):
    """
    Оплата заказа
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status="").first()

        data = {
            "status": order.status,
            "orderId": order.orderId,
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status=2).first()
        if not order:
            order = Order.objects.filter(user=request.user, status=settings.ORDER_STATUSES[1][0]).first()
        number_of_cart = int("".join(request.data.get('number').split()))
        name = request.data.get('name')
        month = request.data.get('month')
        year = request.data.get('year')
        code = request.data.get('code')
        payment_service = PaymentService()
        payment_service.start_payment_processing(num_workers=2)
        # Обработка платежа
        payment_data = payment_service.process_payment(number_of_cart)
        payment_service.payment_queue.join()
        order.status = payment_data['status']
        payment = Payment.objects.create(number=str(number_of_cart), name=name, month=month, year=year, code=code)
        order.payment = payment
        order.save()
        return Response(status=200, template_name="frontend/account.html")

