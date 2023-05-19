from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """
    fullName = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['fullName', 'phone', 'email', 'avatar']

    def get_fullName(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.surname}'


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