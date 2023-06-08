import datetime

from rest_framework import serializers
from order.models import Order, OrderProducts
from product.serializers import ProductSerializer, ProductOrderSerializer

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализация заказа
    """
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', )

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['orderId'] = obj.pk
        data['fullName'] = obj.user.fullName
        data['email'] = obj.user.email
        data['phone'] = obj.user.phone
        data['createdAt'] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        return data


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Сериализация заказа
    """
    # products = ProductOrderSerializer(many=True)


    class Meta:
        model = Order
        fields = ('orderId', 'createdAt', 'fullName', 'email', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["createdAt"] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        return data