from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.contrib import messages
from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse_lazy, reverse
from django.views import View
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from online_store import settings
from account.forms import UserRegistrationForm, LoginForm
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer
from order.models import Order

from account.models import User
from payment.models import PaymentSettings

from payment.serializers import PaymentSettingsSerializer


class AccountUser(APIView):
    """
    API для получения аватара и полного имени.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserAvatarSerializer

    @swagger_auto_schema(
        responses={200: UserAvatarSerializer},
        operation_description=_("Get user full name and avatar"),
    )
    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        print(2323, serializer.data)
        return Response(serializer.data)


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
                    request.session['is_authenticated'] = True
                    if Cart(request).cart:
                        return redirect('cart')
                    return redirect('account')
                    # return redirect(request.get_full_path())
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


class ChangePasswordViewDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class HistoryOrder(View):

    def get(self, request):
        context = {
            'order': Order.objects.all()
        }
        return render(request, 'frontend/historyorder.html', context=context)


class UserProfileView(generics.ListCreateAPIView):
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
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_description="Update user profile",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarView(APIView):
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
    def post(self, request, *args, **kwargs):
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
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            update_session_auth_hash(request, user)  # Обновление сессии после изменения пароля
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(View):
#     def get(self, request):
#         return render(request, 'frontend/profile.html')


class SettingsAPIView(APIView):
    """
    API для получения и обновления настроек.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PaymentSettingsSerializer

    @swagger_auto_schema(
        responses={200: PaymentSettingsSerializer},
        operation_description=_("Get settings"),
    )
    def get(self, request):
        payment_settings = PaymentSettings.objects.first()
        serializer = self.serializer_class(payment_settings)
        settings_data = serializer.data

        # Добавляем возможные выборы для полей
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        is_authenticated = request.user.is_authenticated
        return Response({"is_authenticated": is_authenticated})