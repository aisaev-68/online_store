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
    products = models.ManyToManyField(Product, verbose_name=_('товары в заказе'),
                                      through='OrderProducts', related_name='order_orders')

    createdAt = models.DateField(auto_now_add=True, verbose_name=_('created order'))
    deliveryType = models.BooleanField(default=False, verbose_name=_('availability of free shipping'))
    paymentType = models.TextField(max_length=50, default='credit_card', verbose_name=_('payment method'))
    status = models.TextField(max_length=50, default='В процессе', verbose_name=_('payment state'))
    city = models.TextField(max_length=100, default=_('not specified'), verbose_name=_('delivery city'))
    address = models.TextField(max_length=100, default=_('not specified'), verbose_name=_('delivery address'))
    totalCost = models.IntegerField(default=0, verbose_name=_('total order value'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.city


class OrderProducts(models.Model):
    """
    Модель Продукты в заказе
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('товар из заказа')
        verbose_name_plural = _('все товары из заказа')

    id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('заказ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    count_in_order = models.PositiveIntegerField(default=0, verbose_name=_('количество товара в заказе'))

    def __str__(self):
        """
        Возвращается название товара
        """
        return f'{str(self.product)}'