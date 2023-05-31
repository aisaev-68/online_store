from django.db import models

from online_store import settings


class Payment(models.Model):
    number = models.IntegerField(default=0, verbose_name='номер счета')
    name = models.TextField(max_length=30, default='не указан')
    month = models.DateField(auto_now_add=True)
    year = models.DateField(auto_now_add=True)
    code = models.IntegerField(default=0, verbose_name='код оплаты')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'


class PaymentSettings(models.Model):
    payment_methods = models.CharField(
        max_length=100,
        choices=settings.PAYMENT_METHODS,
        default=settings.PAYMENT_METHODS[0][0]
    )
    shipping_methods = models.CharField(
        max_length=100,
        choices=settings.SHIPPING_METHODS,
        default=settings.SHIPPING_METHODS[0][0]
    )
    order_status = models.CharField(
        max_length=100,
        choices=settings.ORDER_STATUSES,
        default=settings.ORDER_STATUSES[0][0]
    )
    # Дополнительные поля, связанные с настройками оплаты и доставки

    class Meta:
        verbose_name_plural = 'Настройки оплаты и доставки'

