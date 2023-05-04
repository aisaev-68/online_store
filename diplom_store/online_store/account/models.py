import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


def get_upload_path_by_user(instance, filename):
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
    surname = models.CharField(max_length=50, blank=True, verbose_name=_("Surname"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    avatar = models.ImageField(upload_to=get_upload_path_by_user, blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                           validate_image_file_extension], verbose_name=_("Avatar"))

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.fullName:
            self.fullName = f"{self.first_name} {self.last_name} {self.surname}"
        else:
            self.last_name, self.first_name, self.surname = str(self.fullName).split(' ', 2)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
