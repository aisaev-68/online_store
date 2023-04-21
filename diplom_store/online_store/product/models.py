import os

from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from online_shop_app.models import Shop


def get_upload_path_by_products(instance, filename):
    return os.path.join('product_images/', now().date().strftime("%Y/%m/%d"), filename)


class Tag(models.Model):
    tags_name = models.TextField(max_length=50, verbose_name='тэг товара')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.tags_name


# категория товаров
class Category(models.Model):
    title = models.TextField(max_length=50, verbose_name='название категории')
    image = models.FileField(upload_to='my_store_app/static/', null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Specifications(models.Model):
    name = models.TextField(max_length=50, verbose_name='название')
    value = models.TextField(max_length=50, verbose_name='значение')

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return self.name


class Product(models.Model):  # товар
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория товара')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='магазин товара')
    specifications = models.ForeignKey(Specifications, on_delete=models.CASCADE, verbose_name='спецификация товара')
    price = models.IntegerField(default=0, verbose_name='цена товара')
    count = models.IntegerField(default=0, verbose_name='количество ')
    date = models.DateField(auto_now_add=True)
    title = models.TextField(max_length=50, verbose_name='название товара')
    description = models.TextField(max_length=100, verbose_name='описание товара')
    free_delivery = models.BooleanField(default=True)
    product_picture = models.ImageField(upload_to=get_upload_path_by_products, null=True)
    rating = models.IntegerField(default=0, verbose_name='счетчик покупок данного товара')
    tags = models.ManyToManyField(Tag, related_name='tags')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shopapp:products_by_category", kwargs={'tag': self.slug})

