from django.db import models

from account.models import Profile


class OrderHistory(models.Model):  # история покупок пользователя
    user_order = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='пользователь', null=True)
    product_order = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    payment_date = models.DateField(auto_now_add=True)
    delivery_type = models.TextField(max_length=30, default='не указан', verbose_name='способ доставки')
    payment_type = models.TextField(max_length=30, default='не указан', verbose_name='способ оплаты')
    total_cost = models.IntegerField(default=0, verbose_name='общая стоимость заказа')
    status = models.TextField(max_length=30, default='не указан', verbose_name='статус оплаты')
    city = models.TextField(max_length=30, default='не указан', verbose_name='город доставки')
    address = models.TextField(max_length=30, default='не указан', verbose_name='адрес доставки')

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'

    def __str__(self):
        return self.user_order.name


class Order(models.Model):  # покупка товаров из корзины
    product_order = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    count = models.IntegerField(default=0, verbose_name='колличество  товаров в корзине')
    price = models.IntegerField(default=0, verbose_name='общая стоимость  товаров в корзине')
    date = models.DateField(auto_now_add=True)
    free_delivery = models.BooleanField(default=False, verbose_name='наличие бесплатной доставки')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return self.product_order
