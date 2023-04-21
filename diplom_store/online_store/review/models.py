from django.db import models

from account.models import Profile
from product.models import Product


class Reviews(models.Model):  # отзыв
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар',
                                related_name='product_title_product_set')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.CharField(default='Не указано', max_length=100, verbose_name='текст отзыва', blank=True)
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
