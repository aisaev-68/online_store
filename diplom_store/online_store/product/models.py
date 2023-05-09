import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


from catalog.models import Catalog
from catalog.models import Category


def get_upload_path_by_products(instance, filename):
    """
        Получение пути для сохранения изображения продукта
        :param instance: экземпляр продукта
        :param filename: имя файла изображения
        :return: путь для сохранения
        """
    return f'product/images/{instance.product.pk}/{filename}'


class Tag(models.Model):
    name = models.TextField(max_length=50, verbose_name=_('Tag product'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Product(models.Model):  # товар
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Product category'))
    price = models.DecimalField(decimal_places=2, max_digits=10,  verbose_name=_('Price'))
    count = models.IntegerField(default=0, verbose_name=_('Count'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created data'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    fullDescription = models.TextField(max_length=100, verbose_name=_('Full description product'))
    freeDelivery = models.BooleanField(default=False, verbose_name=_('Free shipping')) #бесплатная доставка
    rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True, verbose_name=_('counter of purchases of this product'))
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True, verbose_name=_('Tag'))
    limited = models.BooleanField(default=False, verbose_name=_('Limited edition')) #ограниченный тираж
    banner = models.BooleanField(default=False, verbose_name=_('Banner on home page'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def href(self):
        """
        Получение ссылки для продукта
        :return: ссылка на детальную информацию о продукте
        """
        return f'/product/{self.pk}'

    def description(self):
        """
        Короткое описание продукта
        :return: описание
        """
        if len(self.fullDescription) > 50:
            return f'{self.fullDescription[:50]}...'
        return self.fullDescription

    def photoSrc(self):
        """
        Получение главного изображения продукта
        :return: изображение
        """
        return self.images

    def get_price(self):
        """
        Получение цены продукта в зависимости от наличия скидки
        :return: цена
        """
        salePrice = self.sales.first()  # Если товар есть в таблице с распродажами, то берем цену из этой таблицы
        if salePrice:
            return salePrice.salePrice
        return self.price

    def id(self):
        return f'{self.pk}'

    def __str__(self):
        return self.title



class ProductImage(models.Model):
    """
    Модель изображения продукта
    """
    image = models.FileField(upload_to=get_upload_path_by_products, verbose_name=_('Image product'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Product'))

    class Meta:
        ordering = ["pk"]
        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    def src(self):
        """
        Получаем ссылку на изображение.
        :return: изображение
        """
        return self.image

    def __str__(self):
        return f'/{self.image}'


class Review(models.Model):  # отзыв
    author = models.CharField(max_length=128, verbose_name=_('Author'))
    email = models.EmailField(max_length=254)
    text = models.TextField(verbose_name=_('Text'))
    rate = models.PositiveSmallIntegerField(blank=False, default=5, verbose_name=_('Rating'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created data'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='reviews',
                                verbose_name=_('Product'))

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text

class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales', verbose_name='товар')
    count = models.IntegerField(default=0, verbose_name='количество товара по скидке')
    salePrice = models.IntegerField(default=0, verbose_name='цена распродажи')
    dateFrom = models.DateField()
    dateTo = models.DateField()

    class Meta:
        verbose_name = 'Распродажа'
        verbose_name_plural = 'Распродажа'

    def price(self):
        """
        Получение первоначальной цены продукта
        :return: цена
        """
        return self.product.price

    def images(self):
        """
        Получение изображений продукта
        :return: изображения
        """
        return self.product.images

    def title(self):
        """
        Получение названия продукта
        :return: название продукта
        """
        return self.product.title

    def href(self):
        """
        Получение ссылки на детальную страницу продукта
        :return: ссылка
        """
        return f'/product/{self.product.pk}'

    def __str__(self):
        return self.product.title