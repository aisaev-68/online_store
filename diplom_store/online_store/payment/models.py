from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from online_store import settings
from order.models import Order


class Payment(models.Model):
    number = models.CharField(max_length=16, verbose_name=_('account number'))
    name = models.CharField(max_length=150, verbose_name=_('name'))
    month = models.CharField(max_length=2, verbose_name=_('month'))
    year = models.CharField(max_length=4, verbose_name=_('year'))
    code = models.CharField(max_length=3, verbose_name=_('payment code'))
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order', verbose_name=_('order'), null=True)


    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.number


class PaymentSettings(models.Model):
    payment_methods = models.CharField(
        max_length=100,
        choices=settings.PAYMENT_METHODS,
        default=settings.PAYMENT_METHODS[0][1]
    )
    shipping_methods = models.CharField(
        max_length=100,
        choices=settings.SHIPPING_METHODS,
        default=settings.SHIPPING_METHODS[0][1]
    )
    order_status = models.CharField(
        max_length=100,
        choices=settings.ORDER_STATUSES,
        default=settings.ORDER_STATUSES[2][0]
    )
    page_size = models.IntegerField(
        default=settings.REST_FRAMEWORK['PAGE_SIZE'],
        validators=[MinValueValidator(0)]
    )
    express = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=settings.EXPRESS_SHIPPING_COST,
        verbose_name=_('express price')
    )
    standard = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=settings.STANDARD_SHIPPING_COST,
        verbose_name=_('standard price')
    )
    amount_free = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        default=settings.MIN_AMOUNT_FREE_SHIPPING,
        verbose_name=_('minimum amount free shipping')
    )

    class Meta:
        verbose_name_plural = _('Payment and shipping settings')
