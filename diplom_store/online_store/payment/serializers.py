from . import models
from rest_framework import serializers

from .models import PaymentSettings, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('number', 'name', 'month', 'year', 'code')


class PaymentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSettings
        fields = ('payment_methods', 'shipping_methods', 'order_status', 'page_size', 'express', 'standard', 'amount_free')
