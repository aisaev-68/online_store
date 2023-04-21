import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError




class Sales(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='магазин')
    count = models.IntegerField(default=0, verbose_name='количество товара по скидке')
    dateFrom = models.DateField()
    dateTo = models.DateField()

    class Meta:
        verbose_name = 'Распродажа'
        verbose_name_plural = 'Распродажа'







class Shop(models.Model):
    shop_name = models.TextField(max_length=50, verbose_name='название магазина')

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.shop_name














