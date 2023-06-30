from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse_lazy, reverse
from django.views import View
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from online_store import settings
from account.forms import UserRegistrationForm, LoginForm
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer
from payment.models import PaymentSettings
from account.permissions import IsAdminOrSuperuser
from payment.serializers import PaymentSettingsSerializer


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

        return render(request, 'account/register.html', context)

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
        return render(request, 'account/login.html', context=context)

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
class SettingsAPIView(APIView):
    """
    API для получения и обновления настроек.
    """
    permission_classes = (IsAdminOrSuperuser,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSettingsSerializer

    @swagger_auto_schema(
        responses={200: PaymentSettingsSerializer},
        operation_description=_("Get settings"),
    )
    def get(self, request) -> Response:
        payment_settings = PaymentSettings.objects.first()
        serializer = self.serializer_class(payment_settings)
        settings_data = serializer.data
        print(222, settings_data)

        # Добавляем возможные выборы для полей
        if not settings_data.get('page_size'):
            settings_data['page_size'] = settings.REST_FRAMEWORK['PAGE_SIZE']
        else:
            settings_data['page_size'] = payment_settings.page_size

        if not settings_data.get('express'):
            settings_data['express'] = settings.EXPRESS_SHIPPING_COST
        else:
            settings_data['express'] = payment_settings.express

        if not settings_data.get('standard'):
            settings_data['standard'] = settings.STANDARD_SHIPPING_COST
        else:
            settings_data['standard'] = payment_settings.standard

        if not settings_data.get('amount_free'):
            settings_data['amount_free'] = settings.MIN_AMOUNT_FREE_SHIPPING
        else:
            settings_data['amount_free'] = payment_settings.amount_free

        if not settings_data.get('payment_methods'):
            settings_data['payment_methods'] = settings.PAYMENT_METHODS[0][0]
        else:
            settings_data['payment_methods'] = payment_settings.payment_methods

        if not settings_data.get('shipping_methods'):
            settings_data['shipping_methods'] = settings.SHIPPING_METHODS[0][0]
        else:
            settings_data['shipping_methods'] = payment_settings.shipping_methods

        if not settings_data.get('order_status'):
            settings_data['order_status'] = settings.ORDER_STATUSES[0][0]
        else:
            settings_data['order_status'] = payment_settings.order_status

        if not settings_data.get('filter_min_price'):
            settings_data['filter_min_price'] = settings.FILTER_MIN_PRICE
        else:
            settings_data['filter_min_price'] = payment_settings.filter_min_price

        if not settings_data.get('filter_max_price'):
            settings_data['filter_max_price'] = settings.FILTER_MAX_PRICE
        else:
            settings_data['filter_max_price'] = payment_settings.filter_max_price

        if not settings_data.get('filter_current_from_price'):
            settings_data['filter_current_from_price'] = settings.FILTER_CURRENT_FROM_PRICE
        else:
            settings_data['filter_current_from_price'] = payment_settings.filter_current_from_price

        if not settings_data.get('filter_current_to_price'):
            settings_data['filter_current_to_price'] = settings.FILTER_CURRENT_TO_PRICE
        else:
            settings_data['filter_current_to_price'] = payment_settings.filter_current_to_price

        settings_data['payment_methods_choices'] = dict(settings.PAYMENT_METHODS)
        settings_data['shipping_methods_choices'] = dict(settings.SHIPPING_METHODS)
        settings_data['order_status_choices'] = dict(settings.ORDER_STATUSES)

        return Response(settings_data)

    @swagger_auto_schema(
        request_body=PaymentSettingsSerializer,
        responses={200: PaymentSettingsSerializer},
        operation_description=_("URL of the uploaded settings."),
    )
    def post(self, request):
        payment_settings = PaymentSettings.objects.first()
        serializer = self.serializer_class(payment_settings, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthenticationAPI(APIView):
    """
    Представление API для проверки пользователя на аутентификацию.
    """

    def get(self, request) -> Response:
        is_authenticated = request.user.is_authenticated
        return Response({"is_authenticated": is_authenticated})