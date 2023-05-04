from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField, ReadOnlyPasswordHashField, UserChangeForm, \
    PasswordChangeForm
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


class ChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


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


class UserUpdateForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ('fullName', 'email', 'phone', 'avatar')


class UserUpdateView(forms.Form):
    fullName = forms.CharField(
        required=True,
        label='Full name*:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full name*',
            }
        )
    )

    phone = forms.CharField(required=False, label='Phone number*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone number*',
        }
    ))

    email = forms.CharField(required=True, label='E-mail address*:', widget=forms.EmailInput(
        attrs={
            'placeholder': 'E-mail address*',
        }
    ))
    avatar = forms.CharField(required=False, label='Avatar:', widget=forms.FileInput)


    # class Meta:
    #     model = User
    #     fields = ("avatar", 'fullName', 'email', 'phone',)


class ChangePasswordForm(forms.Form):
    passwordCurrent = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html()
    )
    passwordReply = forms.CharField(
        required=True,
        widget=forms.PasswordInput
    )

    # def clean_password(self):
    #     cd = self.cleaned_data
    #     print(333, cd)
    #     if cd['password'] != cd['passwordReply']:
    #         raise forms.ValidationError('password no match')
    #     return cd['password']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(5555555555555555555555555)
    #     new_password = cleaned_data.get("new_password")
    #     passwordReply = cleaned_data.get("passwordReply")
    #     if new_password != passwordReply:
    #         raise forms.ValidationError(
    #             "New passwords do not match"
    #         )
    #     print(11111111, new_password)
    #     return new_password

