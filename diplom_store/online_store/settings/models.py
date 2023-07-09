from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from online_store import settings



class PaymentSettings(models.Model):
    payment_methods = models.CharField(
        verbose_name=_('payment method'),
        max_length=100,
        choices=settings.PAYMENT_METHODS,
        default=settings.PAYMENT_METHODS[0][1]
    )
    shipping_methods = models.CharField(
        verbose_name=_('shipping method'),
        max_length=100,
        choices=settings.SHIPPING_METHODS,
        default=settings.SHIPPING_METHODS[0][1]
    )
    order_status = models.CharField(
        verbose_name=_('order status'),
        max_length=100,
        choices=settings.ORDER_STATUSES,
        default=settings.ORDER_STATUSES[2][0]
    )
    page_size = models.IntegerField(
        verbose_name=_('page size'),
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
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')