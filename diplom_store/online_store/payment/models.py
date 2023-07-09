from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import F

from order.models import Order


class Payment(models.Model):
    """
    Модель платежей.
    """
    number = models.CharField(max_length=16, verbose_name=_('account number'))
    name = models.CharField(max_length=150, verbose_name=_('name'))
    month = models.CharField(max_length=2, verbose_name=_('month'))
    year = models.CharField(max_length=4, verbose_name=_('year'))
    code = models.CharField(max_length=3, verbose_name=_('payment code'))
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order', verbose_name=_('order'),
                                 null=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def save(self, *args, **kwargs):
        """
        Метод возвращает товар при неудачной оплате
        и изменяет признак available товара, если товары снова доступны.
        :param args:
        :param kwargs:
        :return:
        """
        super().save(*args, **kwargs)
        # Возврат товара при неудачной оплате
        if self.order and self.order.status == 2:
            order_products = self.order.order_products.all()
            for order_product in order_products:
                order_product.product.count = F('count') + order_product.count_product
                if order_product.product.count > 0:
                    order_product.product.available = True
                order_product.product.save()

    def __str__(self):
        return self.number
