import os

from django.db import models
from django.utils.timezone import now


def category_image_directory_path(instance: 'CategoryIcons', filename):
    """
    Получение пути для загрузки иконки категории.
    :param instance: экземпляр класса.
    :param filename: имя загружаемого файла.
    :return: путь для загрузки файла.
    """
    if instance.category.parent:
        return f'category/icons/{instance.category.parent}/{instance.category}/{filename}'
    else:
        return f'category/icons/{instance.category}/{filename}'


def catalog_image_directory_path(instance, filename):
    """
    Получение пути для загрузки иконки каталога
    :param instance: экземпляр класса
    :param filename: имя загружаемого файла
    :return: путь для загрузки файла
    """
    return os.path.join('category/', filename)


class Catalog(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=50, verbose_name='название каталога')
    src = models.FileField(upload_to=catalog_image_directory_path, max_length=500, verbose_name='иконка', blank=True,
                           null=True)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    @property
    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        :return: название иконки
        """
        return f'{self.pk}.png'

    @property
    def href(self):
        if self.src and hasattr(self.src, 'url'):
            return self.src.url

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Модель категории.
    """
    title = models.CharField(max_length=50, verbose_name='название категории')
    src = models.FileField(upload_to=category_image_directory_path, max_length=500, verbose_name='иконка', null=True,
                           blank=True)
    catalog = models.ForeignKey(Catalog, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @property
    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории.
        :return: название иконки.
        """
        return f'{self.pk}.png'

    @property
    def href(self):
        if self.src and hasattr(self.src, 'url'):
            return self.src.url

    def __str__(self):
        return self.title
