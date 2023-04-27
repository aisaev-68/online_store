from django.contrib.auth import login
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from account.models import User
from account.serializers import UserSerializer, UserAvatarSerializer, UserPasswordChangeSerializer


class UserView(viewsets.ModelViewSet):
    """
    Класс представление для получения и обновления данных пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(id=self.request.user.pk)

    def retrieve(self, *args, **kwargs):
        user = User.objects.get(id=self.request.user.pk)
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.data.get('avatar') is not None:
            request.data['avatar'] = request.user.profiles.avatar
        return super().update(request, *args, **kwargs)




class UserAvatarView(viewsets.ModelViewSet):
    """
    Класс представление для обновления аватара пользователя.
    """
    serializer_class = UserAvatarSerializer
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(id=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(avatar=self.request.data['file'])


class UserChangePasswordView(viewsets.ModelViewSet):
    """
    Класс представление для обновления пароля пользователя.
    """
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        login(request, user)
        return Response(serializer.data)
