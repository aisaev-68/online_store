from django.db import models


class Payment(models.Model):
    number = models.IntegerField(default=0, verbose_name='номер счета')
    name = models.TextField(max_length=30, default='не указан')
    month = models.DateField(auto_now_add=True)
    year = models.DateField(auto_now_add=True)
    code = models.IntegerField(default=0, verbose_name='код оплаты')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'
