from . import models
from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежа.
    """
    class Meta:
        model = Payment
        fields = ('number', 'name', 'month', 'year', 'code')
