from django.db import models

from account.models import Profile


class Basket(models.Model):  # корзина пользователя
    username = models.OneToOneField(Profile, unique=True, on_delete=models.CASCADE, related_name='profile')
    product = models.ManyToManyField('Product', related_name='product')
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
