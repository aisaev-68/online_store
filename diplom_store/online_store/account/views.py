import logging
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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from account.forms import UserRegistrationForm, LoginForm
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer


logger = logging.getLogger(__name__)


class AccountUserAPIView(APIView):
    """
    API для получения аватара и полного имени.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = UserAvatarSerializer

    @swagger_auto_schema(
        responses={200: UserAvatarSerializer},
        operation_description=_("Get user full name and avatar"),
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Метод для получения аватара и полного имени.
        :param request:
        :param args:
        :param kwargs:
        :return: Response
        """
        print(99999999999999)
        user = self.request.user
        serializer = self.serializer_class(user)
        logger.info(_('Avatar data successfully serialized!'))
        return Response(serializer.data, status=200)


class RegisterView(View):
    """
    Класс представление для регистрации пользователя.
    """

    def get(self, request, *args, **kwargs):
        """
        Метод для получения формы для регистрации пользователя.
        :param request:
        :param args:
        :param kwargs:
        :return: форма
        """
        form = UserRegistrationForm()

        context = {
            'form': form,
        }
        logger.info(_('User registration form received!'))
        return render(request, 'frontend/register.html', context)

    def post(self, request, *args, **kwargs):
        """
        Метод для регистрации нового пользователя.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
            client_group = Group.objects.get(name="Clients")
            new_user.groups.add(client_group)
            messages.success(request, _('Created profile.'))
            user = authenticate(request, username=new_user, password=password)
            login(request, user)
            logger.info(_(f'User {user} registered!'))
            return redirect('/profile')
        else:
            messages.error(request, _('Profile creation error.'))
            logger.exception(_('Profile creation error!'))
            return render(request, 'account/register.html', context)


class MyLoginView(View):
    """
    Класс представление для авторизации пользователя.
    """
    redirect_authenticated_user = True


    def get(self, request):
        """
        Метод для получение формы входа пользователя.
        :param request:
        :return: форма
        """
        context = {"form": LoginForm()}
        logger.info(_('Getting a login form!'))
        return render(request, 'frontend/login.html', context=context)

    def post(self, request):
        """
        Метод для аутентификации пользователя.
        :param request:
        :return:
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(_('User %s authenticated!'), user.username)
                    if Cart(request).cart:
                        return redirect('cart')
                    return redirect('account')
                else:
                    logger.error(_('Disabled account!'))
                    messages.error(request, _('Disabled account.'))
            else:
                logger.error(_('Password or username does not match!'))
                messages.error(request, _('Password or username does not match.'))
        return redirect('login')


class MyLogoutView(LogoutView):
    """
    Класс представление для выхода пользователя из системы.
    """
    logger.info(_('The user logged out of the personal account!'))
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
        """
        Метод для получения данных профиля.
        :param request:
        :param args:
        :param kwargs:
        :return: сериализированные данные профиля
        """
        serializer = self.serializer_class(self.request.user)
        logger.info(_('User %s profile data obtained!'), request.user.username)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_description=_("Update user profile"),
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Метод для обновление данных профиля.
        :param request:
        :param args:
        :param kwargs:
        :return: сериализированные данные профиля.
        """
        serializer = self.serializer_class(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(_('Update user %s profile!'), request.user.username)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        logger.error(_('Error updating user %s profile!'), request.user.username)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarAPIView(APIView):
    """
    API для обновления аватара.
    """
    parser_classes = [MultiPartParser, ]
    serializer_class = UserAvatarSerializer

    @swagger_auto_schema(
        request_body=UserAvatarSerializer,
        responses={200: UserAvatarSerializer},
        operation_description=_("URL of the uploaded avatar."),
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Метод для обновления аватара.
        :param request:
        :param args:
        :param kwargs:
        :return: url аватара
        """
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(_('Update user %s avatar!'), request.user.username)
            return Response({'url': user.avatar.url})
        logger.error(_('Error updating user %s avatar!'), request.user.username)
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
        """
        Метод для изменения пароля.
        :param request:
        :param args:
        :param kwargs:
        :return: статус выполнения операции.
        """
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            current_password = request.data.get('passwordCurrent')
            user = authenticate(username=request.user.username, password=current_password)
            if user is not None:
                user.set_password(serializer.validated_data['password'])
                user.save()
                logger.info(_('User %s password change!'), user.username)
                update_session_auth_hash(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error(_('User %s password update error!'), request.user.username)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        logger.error(_('User %s password update error!'), request.user.username)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthenticationAPI(APIView):
    """
    Представление API для проверки пользователя на аутентификацию.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    def get(self, request) -> Response:
        """
        Метод проверки пользователя на аутентификацию.
        :param request:
        :return: статус аутентификации.
        """
        is_authenticated = request.user.is_authenticated
        logger.info(_('Checking if a user %s exists!'), request.user.username)
        return Response({"is_authenticated": is_authenticated})