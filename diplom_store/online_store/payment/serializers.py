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
        fields = ('filter_min_price', 'filter_max_price', 'filter_current_from_price', 'filter_current_to_price', 'payment_methods', 'shipping_methods', 'order_status', 'page_size', 'express', 'standard', 'amount_free')
