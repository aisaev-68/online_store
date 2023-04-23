import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from account.managers import CustomUserManager


def get_upload_path_by_user(instance, filename):
    return os.path.join('avatar/', now().date().strftime("%Y/%m/%d"), filename)


class User(AbstractUser):
    def validate_image(self):
        file_size = self.file.size
        megabyte_limit = 2
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(f"Максимальный размер файла не должен превышать {megabyte_limit} МБ")


    first_name = None
    last_name = None
    email = models.EmailField(verbose_name='email address', unique=True)
    fullName = models.CharField(default='не указано', max_length=50, verbose_name='ФИО пользователя', blank=True)
    phone = models.CharField(default='Не указано', max_length=30, verbose_name='номер телефона', blank=True, null=True,
                             unique=True)
    avatar = models.ImageField(upload_to=get_upload_path_by_user, null=True, validators=[validate_image], default='')


    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

