import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


def get_upload_path_by_user(instance, filename):
    return os.path.join('avatar/', now().date().strftime("%Y/%m/%d"), filename)


class CustomUser(AbstractUser):
    def validate_image(self):
        if self.file.size > 2 * 1024 * 1024:
            raise ValidationError("The maximum file size for avatar is 2MB.")

    surname = models.CharField(max_length=50, verbose_name='Surname', blank=True)
    phone = models.CharField(max_length=30, verbose_name='Phone', blank=True, null=True,)
    avatar = models.ImageField(upload_to=get_upload_path_by_user, null=True, validators=[validate_image],
                               default='avatar/default_avatars.png')

    def fullName(self):
        """
        Полное имя
        """
        return f"{self.last_name} {self.first_name} {self.surname}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse("shopapp:catalog_products", kwargs={'eng_name': self.eng_name})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            img.thumbnail((100, 100))
        img.save(self.avatar.path, quality=70, optimize=True)
