import json

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from account.models import User
from online_store import settings
from order.serializers import OrderSerializer, OrderProductSerializer, OrderForAvatarSerializer


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
        order = obj.orders.order_by('-createdAt').first()
        data['order'] = OrderForAvatarSerializer(order).data
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
    passwordCurrent = serializers.CharField()
    passwordReply = serializers.CharField()

    class Meta:
        model = User #settings.AUTH_USER_MODEL
        fields = ['passwordCurrent', 'password', 'passwordReply']

    def save(self, **kwargs):
        self.instance.password = make_password(self.validated_data['password'])
        self.instance.save()
        return self.instance