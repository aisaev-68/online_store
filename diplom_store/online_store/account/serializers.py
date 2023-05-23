from rest_framework import serializers
from drf_yasg import openapi
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """
    # доступно для чтения и записи source='get_fullName', allow_blank=True, required=False
    # fullName = serializers.SerializerMethodField(source='get_fullName', allow_null=True, required=False)
    # avatar = serializers.CharField()
    class Meta:
        model = User
        fields = ['fullName', 'phone', 'email', 'avatar']

    # def get_fullName(self, obj):
    #     return f'{obj.last_name} {obj.first_name} {obj.surname}'

    # def get_field_info(self):
    #     fields = super().get_field_info()
    #     fields['avatar'].schema = openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI)
    #     return fields


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара.
    """
    class Meta:
        model = User
        fields = ['avatar', ]

    def validate_avatar(self, avatar):
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('The image file size should not exceed 2 MB.')
        return avatar

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = User
        fields = ['password']