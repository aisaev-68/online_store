from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from online_store import settings
from order.models import Order

from payment.models import Payment

from payment.serializers import PaymentSerializer


class PaymentView(APIView):
    """
    Оплата заказа
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSerializer

    def post(self, request):
        print("PAYMENT", request.data)
        order = Order.objects.filter(status=_('In progress')).order_by('-createdAt').first()
        number_of_cart = int(''.join(request.data.get('number').split()))
        name = request.data.get('name')
        month = request.data.get('month')
        year = request.data.get('year')
        print(222, settings.ORDER_STATUSES[1])
        if number_of_cart % 2 == 0 and number_of_cart % 10 != 0:
            order.status = settings.ORDER_STATUSES[1]
        else:
            order.status = settings.ORDER_STATUSES[2]
        order.save()
        Payment.objects.create(number=str(number_of_cart), name=name, month=month, year=year)
        return Response(status=200)

