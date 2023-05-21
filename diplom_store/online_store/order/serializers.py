import datetime

from rest_framework import serializers
from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer

from account.serializers import UserSerializer


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
        fields = ('orderId', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost', 'status', 'city', 'address', 'products')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        user = UserSerializer()
        data['orderId'] = str(obj.id)
        data['createdAt'] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        data['fullName'] = user.fullName
        data['email'] = user.email
        data['phone'] = user.phone
        data['deliveryType'] = 'free' if obj.deliveryType else 'not free'
        return data