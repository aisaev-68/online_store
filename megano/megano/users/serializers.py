from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """

    class Meta:
        model = User
        fields = ['fullName', 'phone', 'email', 'avatar']


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара пользователя
    """

    class Meta:
        model = User
        fields = ['avatar']


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = User
        fields = ['password']
