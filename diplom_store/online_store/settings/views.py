import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from online_store import settings
from settings.models import PaymentSettings
from account.permissions import IsAdminOrSuperuser
from settings.serializers import PaymentSettingsSerializer


logger = logging.getLogger(__name__)

class SettingsAPIView(APIView):
    """
    API для получения и обновления настроек.
    """
    permission_classes = (IsAdminOrSuperuser,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSettingsSerializer

    @swagger_auto_schema(
        responses={200: PaymentSettingsSerializer},
        operation_description=_("Get settings"),
    )
    def get(self, request) -> Response:
        payment_settings = PaymentSettings.objects.first()
        serializer = self.serializer_class(payment_settings)
        settings_data = serializer.data

        # Добавляем возможные выборы для полей
        if not settings_data.get('page_size'):
            settings_data['page_size'] = settings.REST_FRAMEWORK['PAGE_SIZE']
        else:
            settings_data['page_size'] = payment_settings.page_size

        if not settings_data.get('express'):
            settings_data['express'] = settings.EXPRESS_SHIPPING_COST
        else:
            settings_data['express'] = payment_settings.express

        if not settings_data.get('standard'):
            settings_data['standard'] = settings.STANDARD_SHIPPING_COST
        else:
            settings_data['standard'] = payment_settings.standard

        if not settings_data.get('amount_free'):
            settings_data['amount_free'] = settings.MIN_AMOUNT_FREE_SHIPPING
        else:
            settings_data['amount_free'] = payment_settings.amount_free

        if not settings_data.get('payment_methods'):
            settings_data['payment_methods'] = settings.PAYMENT_METHODS[0][0]
        else:
            settings_data['payment_methods'] = payment_settings.payment_methods

        if not settings_data.get('shipping_methods'):
            settings_data['shipping_methods'] = settings.SHIPPING_METHODS[0][0]
        else:
            settings_data['shipping_methods'] = payment_settings.shipping_methods

        if not settings_data.get('order_status'):
            settings_data['order_status'] = settings.ORDER_STATUSES[0][0]
        else:
            settings_data['order_status'] = payment_settings.order_status

        settings_data['payment_methods_choices'] = dict(settings.PAYMENT_METHODS)
        settings_data['shipping_methods_choices'] = dict(settings.SHIPPING_METHODS)
        settings_data['order_status_choices'] = dict(settings.ORDER_STATUSES)
        logger.info(_('Getting settings'))
        return Response(settings_data)

    @swagger_auto_schema(
        request_body=PaymentSettingsSerializer,
        responses={200: PaymentSettingsSerializer},
        operation_description=_("URL of the uploaded settings."),
    )
    def post(self, request):
        payment_settings = PaymentSettings.objects.first()
        serializer = self.serializer_class(payment_settings, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        logger.info(_('Save settings'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
