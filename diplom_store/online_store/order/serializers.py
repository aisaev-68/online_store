import datetime

from rest_framework import serializers
from order.models import Order, OrderProducts
from product.serializers import ProductSerializer

#from account.serializers import UserSerializer


# "orderId": "123",
#     "createdAt": "2023-05-05 12:12",
#     "fullName": "Annoying Orange",
#     "email": "no-reply@mail.ru",
#     "phone": "88002000600",
#     "deliveryType": "free",
#     "paymentType": "online",
#     "totalCost": 567.8,
#     "status": "accepted",
#     "city": "Moscow",
#     "address": "red square 1",
#     "products": [

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализация заказа
    """
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('createdAt', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address', 'products')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        # data['orderId'] = obj.pk
        # data['fullName'] = obj.user.fullName
        # data['email'] = obj.user.email
        # data['phone'] = obj.user.phone
        data['createdAt'] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        return data


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['id', 'order', 'product', 'count_in_order']

    def to_representation(self, obj):
        """
        Переопределяет представление модели OrderProducts
        """
        data = super().to_representation(obj)
        return {**data.get('product'), 'count_in_order': data.get('count_in_order')}

class OrderActiveSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('createdAt', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address', 'products')