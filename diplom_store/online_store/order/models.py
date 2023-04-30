from django.db import models

from account.models import CustomUser
from online_store import settings
from product.models import Product


class Order(models.Model):  # Заказы
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    createdAt = models.DateField(auto_now_add=True)
    deliveryType = models.BooleanField(default=False, verbose_name='наличие бесплатной доставки')
    paymentType = models.TextField(max_length=30, default='не указан', verbose_name='способ оплаты')
    status = models.TextField(max_length=30, default='не указан', verbose_name='статус оплаты')
    city = models.TextField(max_length=30, default='не указан', verbose_name='город доставки')
    address = models.TextField(max_length=30, default='не указан', verbose_name='адрес доставки')
    totalCost = models.IntegerField(default=0, verbose_name='общая стоимость заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.products
