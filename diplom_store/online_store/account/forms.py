from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm as ChangeForm, PasswordChangeForm as PassChangeForm
from django.core.exceptions import ValidationError

from account.models import User


class UserRegistrationForm(forms.ModelForm):
    """
    Класс формы регистрации пользователя.
    """
    def __init__(self, *args, **kwargs):
        style = "height: 30px; padding-left: 15px;"
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2',]: #'fullName', 'phone', 'email'
            self.fields[field].widget.attrs['style'] = style


    username = forms.CharField(required=True, label='Username*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username*',
        }
    ))
    # fullName = forms.CharField(required=True, label='Full name*:', widget=forms.TextInput(
    #     attrs={
    #         'placeholder': 'Full name*',
    #     }
    # ))
    # phone = forms.CharField(required=False, label='Phone number*:', widget=forms.TextInput(
    #     attrs={
    #         'placeholder': 'Phone number*',
    #     }
    # ))
    password1 = forms.CharField(required=True, label='Password*:', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password*',
        }
    ),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(required=True, label='Confirm the password*:', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm the password*',
        }
    ))
    # email = forms.CharField(required=True, label='E-mail address*:', widget=forms.EmailInput(
    #     attrs={
    #         'placeholder': 'E-mail address*',
    #     }
    # ))
    # avatar = forms.CharField(required=False, label='Avatar:', widget=forms.FileInput)

    error_messages = {
        "password_mismatch": "Пароли не совпадают! Повторите ввод!",
        # "phone_exists": "Пользователь с таким номером телефона уже существует!",
        # "email_exists": "Пользователь с таким email уже существует!",
    }

    class Meta:
        model = User
        # fields = ('username', 'fullName', 'email', 'phone', 'password', 'password1', "avatar")

        fields = ('username', 'password1', 'password2', )


    def clean_password(self):
        cd = self.cleaned_data
        print(333, cd)
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('password no match')
        return cd['password1']

    # def clean_phone(self):
    #     """
    #     Метод для определение уникальности номера телефона.
    #     :return: phone
    #     """
    #     phone = self.cleaned_data.get('phone')
    #     if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError("This phone number is already in use.")
    #     return phone
    #
    # def clean_email(self):
    #     """
    #     Метод для определения уникальности email.
    #     :return: email
    #     """
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email
    #
    # def clean_username(self):
    #     """
    #     Метод для определения уникальности username.
    #     :return: username
    #     """
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError("This username is already in use.")
    #     return username
    #
    # def clean_avatar(self):
    #     avatar = self.cleaned_data.get('avatar')
    #     if avatar and avatar.size > 2 * 1024 * 1024:
    #         raise forms.ValidationError("The maximum file size for avatar is 2MB.")
    #     return avatar


# class UserChangeForm(ChangeForm):
#     class Meta:
#         model = User
#         fields = ['fullName', 'email', 'phone', 'avatar']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username*',
            }
        ),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Password*',
                'help_text': ''
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['style'] = "height: 30px; padding-left: 5px;"
        self.fields['password'].widget.attrs['style'] = "height: 30px; padding-left: 5px;"


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['fullName', 'email', 'phone', 'avatar']
#
#     def __init__(self, *args, **kwargs):
#         super(UserUpdateForm, self).__init__(*args, **kwargs)
#         self.fields['avatar'].widget.attrs.update({'class': 'form-control-file'})
#         self.fields['email'].widget.attrs.update({'class': 'form-control', 'readonly': True})
#         self.fields['fullName'].widget.attrs.update({'class': 'form-control'})
#         self.fields['phone'].widget.attrs.update({'class': 'form-control'})
#
#     def clean(self):
#         cleaned_data = super().clean()
#         self.instance.clean_avatar()
#         return cleaned_data

class UserUpdateView(forms.Form):
    fullName = forms.CharField(
        required=True,
        label='Full name*:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full name*',
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(required=False, label='Phone number*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone number*',
            'class': 'form-control',
        }
    ))

    email = forms.CharField(required=True, label='E-mail address*:', widget=forms.EmailInput(
        attrs={
            'placeholder': 'E-mail address*',
            'class': 'form-control',
        }
    ))
    avatar = forms.CharField(required=False, label='Avatar:', widget=forms.FileInput)


    # class Meta:
    #     model = User
    #     fields = ("avatar", 'fullName', 'email', 'phone',)


class PasswordChangeForm(PassChangeForm):
    old_password = forms.CharField(
        required=True,
        label='Old password:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Old_password*',
            }
        ),
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password1 = forms.CharField(
        required=True,
        label='New password:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password*',
            }
        ),
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        required=True,
        label='New password confirmation:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password confirmation*',
            }
        )
    )





