from . import models
from rest_framework import serializers

from .models import PaymentSettings


class PaymentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSettings
        fields = ('payment_methods', 'shipping_methods', 'order_status', 'page_size')
