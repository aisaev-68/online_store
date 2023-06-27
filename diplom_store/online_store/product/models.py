from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


from catalog.models import Category
from tag.models import Tag


def get_upload_path_by_products(instance, filename):
    """
        Получение пути для сохранения изображения продукта
        :param instance: экземпляр продукта
        :param filename: имя файла изображения
        :return: путь для сохранения
        """
    return f'product_images/"%Y/%m/%d"/{filename}'


class Product(models.Model):  # товар
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('product category'))
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('price'))
    count = models.IntegerField(default=0, verbose_name=_('quantity'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('created data'))
    title = models.CharField(max_length=150, verbose_name=_('title'))
    fullDescription = models.TextField(max_length=100, verbose_name=_('full description product'))
    freeDelivery = models.BooleanField(default=False, verbose_name=_('free shipping'))  # бесплатная доставка
    limited = models.BooleanField(default=False, verbose_name=_('limited edition'))  # ограниченный тираж
    banner = models.BooleanField(default=False, verbose_name=_('banner on home page'))
    available = models.BooleanField(default=True, verbose_name=_('available'))
    brand = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, related_name='products', verbose_name='manufacturer')
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='products',
                              verbose_name='seller')
    attributes = models.JSONField(default=dict, blank=True, verbose_name=_('attributes'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tag'), blank=True, related_name='product_tags')

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
        self.count -= quantity_sold

        if self.count == 0:
            self.available = False

        self.save()

    def rating_info(self):
        return self.reviews.aggregate(avg_rating=models.Avg('rate')).get('avg_rating')

    def reviews_list(self):
        return list(self.reviews.all())

    def href(self):
        """
        Получение ссылки для продукта
        :return: ссылка на детальную информацию о продукте
        """
        return f'/product/{self.pk}/'

    def description(self):
        """
        Короткое описание продукта
        :return: описание
        """
        if len(self.fullDescription) > 50:
            return f'{self.fullDescription[:50]}...'
        return self.fullDescription

    def photo(self):
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

    # def id(self):
    #     return f'{self.pk}'

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
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name=_('rate'))
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



class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales', verbose_name=_('product'))
    count = models.IntegerField(default=0, verbose_name=_('quantity of goods at a discount'))
    salePrice = models.IntegerField(default=0, verbose_name=_('sale price'))
    dateFrom = models.DateField()
    dateTo = models.DateField()

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')

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


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name'))

    class Meta:
        verbose_name = _('manufacturer')
        verbose_name_plural = _('manufacturers')

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name'))
    city = models.TextField(max_length=100, verbose_name=_('city'))
    address = models.TextField(max_length=100, verbose_name=_('address'))

    class Meta:
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')

    def __str__(self):
        return self.name



class Specification(models.Model):
    attributes = models.JSONField(default=dict, blank=True, verbose_name=_('attributes'))
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='specifications', verbose_name=_('category'))

    class Meta:
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')

    def __str__(self):
        return str(self.attributes)