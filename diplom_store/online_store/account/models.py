import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.utils.timezone import now


def get_upload_path_by_user(filename):
    """
    Функция возврата пути файла.
    :param filename:
    :return: возвращает путь для записи файла
    """
    return os.path.join('avatar/', now().date().strftime("%Y/%m/%d"), filename)


def validate_image_file_extension(image):
    """
    Валидатор, проверяющий размер изображения
    """
    max_size = 2 * 1024 * 1024  # 2 Мб
    if image.size > max_size:
        raise ValidationError(
            _(f'The image exceeds the maximum size in {max_size / (1024 * 1024)} Mb'))


class User(AbstractUser):
    fullName = models.CharField(max_length=100, blank=True, verbose_name=_("Full name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    surname = models.CharField(max_length=50, blank=True, verbose_name=_("Surname"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"), unique=True)
    avatar = models.ImageField(upload_to=get_upload_path_by_user, blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                           validate_image_file_extension], verbose_name=_("Avatar"))

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.fullName:
            self.last_name, self.first_name, self.surname = str(self.fullName).split(' ', 2)
        else:
            self.fullName = f'{self.last_name} {self.first_name} {self.surname}'
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            existing_user = User.objects.get(phone=self.phone)
            if existing_user and existing_user.id != self.id:
                raise ValidationError(_("Phone number already exists."))
        except User.DoesNotExist:
            pass

        try:
            existing_user = User.objects.get(email=self.email)
            if existing_user and existing_user.id != self.id:
                raise ValidationError(_("Email already exists."))
        except User.DoesNotExist:
            pass

    def clean_avatar(self):
        if self.avatar:
            if self.avatar.size > 2 * 1024 * 1024:
                raise ValidationError(_('The image file size should not exceed 2 MB.'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
