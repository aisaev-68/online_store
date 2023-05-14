from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import UserChangeForm

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(request.user)
        return render(request, 'account/profile.html', {'user': user, 'form': form, 'password_form': password_form})

    def post(self, request):
        user = request.user
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        print(111, form)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('account:profile')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated successfully.')
            return redirect('account:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/profile.html', {'user': user, 'form': form, 'password_form': password_form})
