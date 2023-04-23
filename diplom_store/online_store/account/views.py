from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.forms import UserRegistrationForm
from account.models import User
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer


class RegisterView(CreateView):
    """
    Класс представление для регистрации пользователя.
    """
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy('frontend:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        User.objects.create(user=self.object, fullName=form.cleaned_data.get('fullName'),
                            phone=form.cleaned_data.get('phone'), email=form.cleaned_data.get('email'))
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response


class UserView(viewsets.ModelViewSet):
    """
    Класс представление для получения и обновления данных пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(user_id=self.request.user.pk)

    def retrieve(self, *args, **kwargs):
        user = User.objects.get(user_id=self.request.user.pk)
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
        return User.objects.get(user_id=self.request.user.pk)

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


class MyLoginView(LoginView):
    """
    Класс представление для авторизации пользователя.
    """
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    """
    Класс представление для выхода пользователя из системы
    """
    next_page = reverse_lazy('account:login')
