from django.db import models
from django.utils.translation import gettext_lazy as _
from online_store import settings
from product.models import Product


class Order(models.Model):  # Заказы
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_('user'),
        null=True
    )
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    createdAt = models.DateField(auto_now_add=True, verbose_name=_('created order'))
    deliveryType = models.BooleanField(default=False, verbose_name=_('availability of free shipping'))
    paymentType = models.TextField(max_length=30, default=_('not specified'), verbose_name=_('payment method'))
    status = models.TextField(max_length=30, default=_('not specified'), verbose_name=_('payment state'))
    city = models.TextField(max_length=30, default=_('not specified'), verbose_name=_('delivery city'))
    address = models.TextField(max_length=30, default=_('not specified'), verbose_name=_('delivery address'))
    totalCost = models.IntegerField(default=0, verbose_name=_('total order value'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.products
