from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError


class Profile(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        megabyte_limit = 150.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла {}MB".format(str(megabyte_limit)))

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(default='-------', max_length=50,
                                verbose_name='username', blank=True, null=True)
    full_name = models.CharField(default='не указано', max_length=50, verbose_name='ФИО пользователя', blank=True)
    phone = models.CharField(default='Не указано', max_length=30, verbose_name='номер телефона', blank=True, null=True,
                             unique=True)
    email = models.EmailField(verbose_name='email пользователя', blank=True, unique=True)
    avatar = models.ImageField(upload_to='catalog/files/', null=True, validators=[validate_image], default='')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Profile.objects.create(user=instance)
