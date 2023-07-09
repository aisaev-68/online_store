from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse_lazy
from django.views import View
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from account.forms import UserRegistrationForm, LoginForm
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer



class AccountUserAPIView(APIView):
    """
    API для получения аватара и полного имени.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserAvatarSerializer

    # @swagger_auto_schema(
    #     responses={200: UserAvatarSerializer},
    #     operation_description=_("Get user full name and avatar"),
    # )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Метод для получения аватара и полного имени.
        :param request:
        :param args:
        :param kwargs:
        :return: Response
        """
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)


class RegisterView(View):
    """
    Класс представление для регистрации пользователя.
    """

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()

        context = {
            'form': form,
        }

        return render(request, 'frontend/register.html', context)

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(
            request.POST,
        )

        context = {
            'form': form,
        }

        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data['password1']
            new_user.set_password(password)
            new_user.save()
            # client_group = Group.objects.get(name="Clients")
            # new_user.groups.add(client_group)
            messages.success(request, _('Created profile.'))
            user = authenticate(request, username=new_user, password=password)
            login(request, user)
            # return redirect(reverse('account:profile'))
            return redirect('/profile')
        else:
            messages.error(request, _('Profile creation error.'))

            return render(request, 'account/register.html', context)


class MyLoginView(View):
    """
    Класс представление для авторизации пользователя.
    """
    redirect_authenticated_user = True


    def get(self, request):
        context = {"form": LoginForm()}
        return render(request, 'frontend/login.html', context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if Cart(request).cart:
                        return redirect('cart')
                    return redirect('account')
                else:
                    messages.error(request, _('Disabled account.'))
            else:
                messages.error(request, _('Password or username does not match.'))
        return redirect('login')


class MyLogoutView(LogoutView):
    """
    Класс представление для выхода пользователя из системы.
    """
    next_page = reverse_lazy('login')


class UserProfileAPIView(generics.ListCreateAPIView):
    """
    API для получения и обновления профиля пользователя.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_description=_("Get user profile"),
    )
    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_description=_("Update user profile"),
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarAPIView(APIView):
    """
    API для обновления автара.
    """
    parser_classes = [MultiPartParser, ]
    serializer_class = UserAvatarSerializer

    @swagger_auto_schema(
        request_body=UserAvatarSerializer,
        responses={200: UserAvatarSerializer},
        operation_description=_("URL of the uploaded avatar."),
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'url': user.avatar.url})
        return Response(serializer.errors, status=400)


class UserPasswordChangeView(APIView):
    """
    API для обновления пароля пользователя.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserPasswordChangeSerializer

    @swagger_auto_schema(
        request_body=UserPasswordChangeSerializer,
        responses={200: UserPasswordChangeSerializer},
        operation_description=_("URL of the uploaded password."),
    )
    def post(self, request, *args, **kwargs) -> Response:
        print('request.data', request.data)
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            current_password = request.data.get('passwordCurrent')
            user = authenticate(username=request.user.username, password=current_password)
            if user is not None:
                user.set_password(serializer.validated_data['password'])
                user.save()
                print('PASSWORD', user.password)
                update_session_auth_hash(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthenticationAPI(APIView):
    """
    Представление API для проверки пользователя на аутентификацию.
    """

    def get(self, request) -> Response:
        is_authenticated = request.user.is_authenticated
        return Response({"is_authenticated": is_authenticated})