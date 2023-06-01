from django.http import HttpResponse
from rest_framework.views import APIView

from online_store import settings
from order.models import Order


class PaymentView(APIView):
    """
    Оплата заказа
    """
    def post(self, request):
        order = Order.objects.get(pk=request.data.get('order'))
        number_of_cart = int(''.join(request.data.get('number').split()))
        if number_of_cart % 2 == 0 and number_of_cart % 10 != 0:
            order.status = settings.status[1]
        else:
            order.status = settings.status[2]
        order.save()
        return HttpResponse()

