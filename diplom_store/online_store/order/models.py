from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from online_store import settings
from product.models import Product


class Order(models.Model):  # Заказы
    orderId = models.AutoField(primary_key=True, unique=True, verbose_name=_('order number'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_('user'),
        null=True
    )
    products = models.ManyToManyField(Product, verbose_name=_('goods in order'),
                                      through='OrderProducts', related_name='order_products')

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name=_('created order'))
    fullName = models.CharField(max_length=100, default='', verbose_name=_('full name'))
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(max_length=16,
                             validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")], verbose_name=_('phone'))
    deliveryType = models.CharField(max_length=50, choices=settings.SHIPPING_METHODS, verbose_name=_('availability of free shipping'))
    paymentType = models.CharField(max_length=50, choices=settings.PAYMENT_METHODS, verbose_name=_('payment method'))
    status = models.TextField(max_length=50, choices=settings.ORDER_STATUSES, verbose_name=_('payment state'))
    city = models.CharField(max_length=50, default=_('not specified'), verbose_name=_('delivery city'))
    address = models.CharField(max_length=100, default=_('not specified'), verbose_name=_('delivery address'), blank=True)
    totalCost = models.IntegerField(default=0, verbose_name=_('total order value'), blank=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return '{}{}'.format(_('Order № '), self.orderId)


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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    count_product = models.PositiveIntegerField(default=0, verbose_name=_('quantity of goods in the order'))

    def __str__(self):
        """
        Возвращается название товара
        """
        return f'{str(self.product)}'