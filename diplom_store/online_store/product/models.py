import os

from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from account.models import User
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
    name = models.TextField(max_length=50, verbose_name='тэг товара')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


# категория товаров

class Specification(models.Model):
    name = models.TextField(max_length=50, verbose_name='название')
    value = models.TextField(max_length=50, verbose_name='значение')

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return self.name


class Product(models.Model):  # товар
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория товара')
    specifications = models.ForeignKey(Specification, on_delete=models.CASCADE, verbose_name='спецификация товара')
    price = models.IntegerField(default=0, verbose_name='цена товара')
    count = models.IntegerField(default=0, verbose_name='количество ')
    date = models.DateField(auto_now_add=True)
    title = models.TextField(max_length=50, verbose_name='название товара')
    fullDescription = models.TextField(max_length=100, verbose_name='полное описание товара')
    freeDelivery = models.BooleanField(default=True)
    rating = models.IntegerField(default=0, verbose_name='счетчик покупок данного товара')
    tags = models.ManyToManyField(Tag, related_name='tags')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

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
    image = models.FileField(upload_to=get_upload_path_by_products, verbose_name='изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='продукт')

    class Meta:
        ordering = ["pk"]
        verbose_name = "изображение продукта"
        verbose_name_plural = "изображения продуктов"

    def src(self):
        """
        Получаем ссылку на изображение.
        :return: изображение
        """
        return self.image

    def __str__(self):
        return f'/{self.image}'


class Review(models.Model):  # отзыв
    author = models.CharField(max_length=128, verbose_name='автор')
    email = models.EmailField(max_length=254)
    text = models.TextField(verbose_name='текст')
    rate = models.PositiveSmallIntegerField(blank=False, default=5, verbose_name='оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='reviews',
                                verbose_name='продукт')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

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