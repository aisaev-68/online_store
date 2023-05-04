from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import request, HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from account.forms import UserRegistrationForm, LoginForm, UserUpdateForm, ChangePasswordForm
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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # password_form = ChangePasswordForm()
        password_form = PasswordChangeForm(request.user)
        form = UserUpdateForm(initial={'phone': user.phone,
                                       'avatar': user.avatar,
                                       'fullName': user.last_name + ' ' + user.first_name + ' ' + user.surname,
                                       'email': user.email,})

        return render(request, 'account/profile.html', context={'form': form, 'password_form': password_form})

    def post(self, request, *args, **kwargs):
        user = request.user
        password_form = PasswordChangeForm(user, request.POST)
        # password_form = ChangePasswordForm(request.POST)
        form = UserUpdateForm(request.POST, request.FILES, user)

        if password_form.is_valid():
            print(11111, password_form.cleaned_data)
            update_session_auth_hash(request, password_form.save())
            messages.success(request, _('Your password was successfully updated!'))
            # old_password = password_form.cleaned_data["passwordCurrent"]
            # new_password = password_form.cleaned_data["new_password"]
            # print(6666, old_password, new_password)
            # if user.check_password(old_password):
            #     user.set_password(new_password)
            #     user.save()
            #     update_session_auth_hash(request, user)
            # return redirect('account:profile')
        else:
            return HttpResponse('bad')
        if form.is_valid():

            print(222, form)
            avatar = request.FILES.get('avatar')
            # last_name, first_name, surname = form.cleaned_data['fullName'].split(' ', 2)
            # user.last_name, user.first_name, user.surname = last_name, first_name, surname
            # user.email = form.cleaned_data['email']
            # user.phone = form.cleaned_data['phone']
            user.avatar = avatar
            print(55555, user.email, user.phone)
            user.save()
        return redirect('account:profile')
        # return render(request, 'account/profile.html', context={'form': UserUpdateForm(instance=request.user), 'password_form': PasswordChangeForm(request.user)})


class UserAvatarView(View):
    pass

#
# class ChangePasswordView(View):
#     def post(self, request, *args, **kwargs):
#         user = User.objects.get(username=request.user)
#         form = ChangePasswordForm(request.POST)
#         if form.is_valid():
#             old_password = request.POST.get("passwordCurrent")
#             new_pass = request.POST.get("new_password")
#             new_pass_rep = request.POST.get("passwordReply")
#             if check_password(old_password, user.password):
#                 user.set_password(new_pass)
#                 user.save()
#                 return HttpResponse('ok')
#             else:
#                 return HttpResponse('bad')
#         else:
#             form = ChangePasswordForm()
#             return render(request, 'account/profile.html',
#                   {'form': form, 'user': user})