from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from account.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Класс формы регистрации пользователя.
    """
    username = forms.CharField(required=True, label='Username*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username*',
        }
    ))
    fullName = forms.CharField(required=True, label='Full name*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Full name*',
        }
    ))
    phone = forms.CharField(required=True, label='Phone number*:', widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone number*',
        }
    ))
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
    email = forms.CharField(required=True, label='E-mail address*:', widget=forms.EmailInput(
        attrs={
            'placeholder': 'E-mail address*',
        }
    ))
    avatar = forms.CharField(required=False, label='Avatar:', widget=forms.FileInput)

    error_messages = {
        "password_mismatch": "Пароли не совпадают! Повторите ввод!",
        "phone_exists": "Пользователь с таким номером телефона уже существует!",
        "email_exists": "Пользователь с таким email уже существует!",
    }

    class Meta:
        model = User
        fields = ('username', 'fullName', 'email', 'phone', 'password1', 'password2', "avatar")
        # field_classes = {"username": UsernameField}

    def clean_phone(self):
        """
        Метод для определение уникальности номера телефона.
        :return: phone
        """
        phone = self.cleaned_data.get("phone")
        phone_db = User.objects.filter(phone=phone)
        if phone_db:
            raise ValidationError(
                self.error_messages["phone_exists"],
                code="phone_exists",
            )
        return phone

    def clean_email(self):
        """
        Метод для определения уникальности email.
        :return: email
        """
        email = self.cleaned_data.get("email")
        email_db = User.objects.filter(email=email)
        if email_db:
            raise ValidationError(
                self.error_messages["email_exists"],
                code="email_exists",
            )
        return email


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
        self.fields['username'].widget.attrs['style'] = "height: 30px;"
        self.fields['password'].widget.attrs['style'] = "height: 30px;"
