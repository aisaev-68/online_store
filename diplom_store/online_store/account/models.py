import os
from PIL import Image
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



    surname = models.CharField(default='не указано', max_length=50, verbose_name='Surname', blank=True)
    phone = models.CharField(default='Не указано', max_length=30, verbose_name='Phone', blank=True, null=True,
                             unique=True)
    avatar = models.ImageField(upload_to=get_upload_path_by_user, null=True, validators=[validate_image], default='avatar/default_avatars.png')

    objects = CustomUserManager()
    def fullName(self):
        """
        Полное имя
        """
        return f"{self.last_name} {self.first_name} {self.surname}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            img.thumbnail((100, 100))
        img.save(self.avatar.path, quality=70, optimize=True)