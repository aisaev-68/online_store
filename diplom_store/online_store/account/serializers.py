from rest_framework import serializers

from account.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """

    class Meta:
        model = CustomUser
        fields = ['fullName', 'phone', 'email', 'avatar']


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара пользователя
    """

    class Meta:
        model = CustomUser
        fields = ['avatar']


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = CustomUser
        fields = ['password']