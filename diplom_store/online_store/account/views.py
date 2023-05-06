from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import request, HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from account.forms import UserRegistrationForm, LoginForm, UserUpdateForm
from account.models import User
from account.serializers import UserPasswordChangeSerializer, UserAvatarSerializer, UserSerializer


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
            # messages.success(request, _('Created profile.'))
            user = authenticate(request, username=new_user, password=password)
            login(request, user)
            return redirect(reverse('account:profile'))
        else:
            # messages.error(request, _('Profile creation error.'))

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
                    return redirect(reverse('account:profile'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class MyLogoutView(LogoutView):
    """
    Класс представление для выхода пользователя из системы
    """
    next_page = reverse_lazy('account:login')


class ChangePasswordViewDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class UserAvatarView(View):
    def get(self, request, *args, **kwargs):
        print(8888, request.user.avatar)
        return render(request, 'account/account.html')


class UpdateProfileView(View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'account/profile.html', {'user_form': user_form, 'password_form': password_form})

    def post(self, request):
        if 'fullName' in request.POST:
            user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, _('Your profile was updated successfully.'))
                return redirect('account:profile')
            else:
                if user_form.errors.get('avatar'):
                    messages.error(request, user_form.errors['avatar'])
                elif user_form.errors.get('email'):
                    messages.error(request, user_form.errors['email'])
                else:
                    messages.error(request, _('There was an error updating your profile. Please try again.'))
        elif 'new_password1' in request.POST:
            password_form = PasswordChangeForm(data=request.POST, user=request.user)

            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, _('Your password was updated successfully.'))
                return redirect('account:profile')
            else:
                if password_form.errors.get('old_password'):
                    messages.error(request, _('Your old password was entered incorrectly. Please enter it again.'))
                else:
                    messages.error(request, _('The two password fields didn’t match.'))
        else:
            messages.error(request, _('Invalid request. Please try again.'))
        return redirect('account:profile')
