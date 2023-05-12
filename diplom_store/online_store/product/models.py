import os
from django.utils.translation import gettext_lazy as _
from django.db import models
import django_filters
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


# class Tag(models.Model):
#     name = models.TextField(max_length=50, verbose_name=_('Tag product'))
#     tags = models.ManyToManyField('Tag', related_name='tags', blank=True, verbose_name=_('Tag'))
#
#     class Meta:
#         verbose_name = _('tag')
#         verbose_name_plural = _('tags')
#
#     def __str__(self):
#         return self.name


class Product(models.Model):  # товар
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Product category'))
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('Price'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created data'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    fullDescription = models.TextField(max_length=100, verbose_name=_('Full description product'))
    freeDelivery = models.BooleanField(default=False, verbose_name=_('Free shipping'))  # бесплатная доставка
    tag = models.SlugField(max_length=200, db_index=True, verbose_name=_('Tag product'))
    limited = models.BooleanField(default=False, verbose_name=_('Limited edition'))  # ограниченный тираж
    banner = models.BooleanField(default=False, verbose_name=_('Banner on home page'))
    brand = models.CharField(max_length=100, verbose_name=_('Brand'))
    attributes = models.JSONField(default=dict, blank=True, verbose_name=_('Attributes'))
    in_stock = models.BooleanField(default=True, verbose_name=_('In stock'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def sell(self, quantity_sold):
        """
        Метод sell уменьшает количество товаров при продаже
        и изменяет признак in_stock, если товары закончились.
        :param quantity_sold:
        :return:
        """
        self.quantity -= quantity_sold

        if self.quantity == 0:
            self.in_stock = False

        self.save()

    def rating_info(self):
        rating_info = getattr(self, 'rating_info', None)
        if rating_info is None:
            return {
                'rating': None,
                'count': 0,
            }
        return {
            'rating': rating_info.rating,
            'count': rating_info.count,
        }

    def reviews_list(self):
        return list(self.reviews.all())

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
        return self.images.all()[0]

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


class ProductFilter(django_filters.FilterSet):
    CHOICES = [
        ["title", "по названию"],
        ["price", "дешевые сверху"],
        ["-price", "дорогие сверху"]
    ]
    title = django_filters.CharFilter(name='name', lookup_expr='icontains')
    category__slug = django_filters.CharFilter()
    price__gt = django_filters.NumberFilter(name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(name='price', lookup_expr='lt')
    ordering = django_filters.OrderingFilter(choices=CHOICES, required=True, empty_label=None,)

    class Meta:
        model = Product
        exclude = [field.name for field in Product._meta.fields]
        order_by_field = 'title'

class Rating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating_info')
    rating = models.DecimalField(decimal_places=1, max_digits=2, verbose_name=_('rating'))
    count = models.PositiveIntegerField(default=0, verbose_name=_('count'))

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')


class Review(models.Model):  # отзыв
    author = models.CharField(max_length=128, verbose_name=_('author'))
    email = models.EmailField(max_length=254)
    text = models.TextField(verbose_name=_('Text'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('created data'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews',
                                verbose_name=_('product'))

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        rating_info, created = Rating.objects.get_or_create(product=self.product)
        rating_info.count = self.product.reviews.count()
        rating_info.rating = self.product.reviews.aggregate(models.Avg('rating'))['rating__avg']
        rating_info.save()


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
