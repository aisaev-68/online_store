from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from account.models import User

style = "min-height: 45px; padding-left: 15px;"
margin_stile = "margin-top: 15px;"

class UserRegistrationForm(forms.ModelForm):
    """
    Класс формы регистрации пользователя.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = style


    username = forms.CharField(
        required=True,
        label=_('Username*:'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Username*'),
            }
        )
    )

    phone = forms.CharField(
        required=True,
        label=_('Phone number*:'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Phone number*'),
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        label=_('Password*:'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Password*'),
            }
        ),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        required=True,
        label=_('Confirm the password*:'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Confirm the password*'),
            }
        )
    )
    email = forms.CharField(
        required=True,
        label=_('E-mail address*:'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('E-mail address*'),
            }
        )
    )

    error_messages = {
        "password_mismatch": _("Password mismatch! Retype!"),
        "phone_exists": _("A user with this phone number already exists!"),
        "email_exists": _("A user with this email already exists!"),
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2',)

    def clean_password(self):
        cd = self.cleaned_data

        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('password no match')
        return cd['password1']

    def clean_phone(self):
        """
        Метод для определение уникальности номера телефона.
        :return: phone
        """
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This phone number is already in use."))
        return phone

    def clean_email(self):
        """
        Метод для определения уникальности email.
        :return: email
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This email is already in use."))
        return email


class LoginForm(forms.Form):
    """
    Класс формы ввода пароля и логина.
    """
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Username*'),
            }
        ),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Password*'),
                'help_text': ''
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = style

