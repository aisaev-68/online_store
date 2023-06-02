import json

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from account.models import User
from order.serializers import OrderSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """

    class Meta:
        model = User
        fields = ['fullName', 'phone', 'email', 'avatar']




class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара.
    """
    class Meta:
        model = User
        fields = ['avatar', 'last_name', 'first_name', 'surname']

    def to_representation(self, obj):
        data = super().to_representation(obj)
        orders = obj.orders.order_by('-createdAt')
        data['orders'] = OrderSerializer(orders, many=True).data
        print('GGGG', data)
        # data['orders'] = [{
        #     "orderId": str(order.id),
        #     "createdAt": order.createdAt.strftime("%Y-%m-%d %H:%M"),
        #     "deliveryType": "free" if order.deliveryType else "not free",
        #     "paymentType": order.paymentType,
        #     "totalCost": float(order.totalCost),
        #     "status": order.status,
        #     "products":  order.products.all()
        # }]
        return data

    def validate_avatar(self, avatar):
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('The image file size should not exceed 2 MB.')
        return avatar

    def update(self,obj, validated_data):
        obj.avatar = validated_data.get('avatar', obj.avatar)
        obj.save()
        return obj

class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = User
        fields = ['password']

    def save(self, **kwargs):
        self.instance.password = make_password(self.validated_data['password'])
        self.instance.save()
        return self.instance