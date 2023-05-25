import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


def get_upload_path_by_catalog(instance, filename):
    """
        Получение пути для сохранения изображения продукта
        :param instance: экземпляр продукта
        :param filename: имя файла изображения
        :return: путь для сохранения
        """
    return f'catalog/{filename}'


def get_upload_path_by_category(instance, filename):
    """
        Получение пути для сохранения изображения продукта
        :param instance: экземпляр продукта
        :param filename: имя файла изображения
        :return: путь для сохранения
        """
    return f'category/{filename}'


class Catalog(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=128, db_index=True, verbose_name=_('catalog'))


    class Meta:
        ordering = ["title", "pk"]
        verbose_name = _("catalog")
        verbose_name_plural = _("catalogs")

    def href(self):
        """
        Получение ссылки
        :return: ссылка
        """
        return f'/catalog/{self.pk}'

    def __str__(self):
        return self.title


class CatalogIcons(models.Model):
    """
    Модель иконки категории
    """
    src = models.FileField(upload_to=get_upload_path_by_catalog, max_length=500, verbose_name=_('icon'))
    catalog = models.OneToOneField(
        Catalog,
        on_delete=models.CASCADE,
        related_name='image',
        verbose_name=_('catalog'),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = _("icon catalog")
        verbose_name_plural = _("icons catalogs")

    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        :return: название иконки
        """
        return self.catalog.title

    def __str__(self):
        return f'{self.pk} icon'

class Category(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=128, db_index=True, verbose_name=_('category'))
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name=_('catalog'),
    )
    active = models.BooleanField(default=False, verbose_name=_('active'))

    class Meta:
        ordering = ["title", "pk"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def href(self):
        """
        Получение ссылки
        :return: ссылка
        """
        return f'/catalog/{self.pk}'

    def __str__(self):
        return self.title


class CategoryIcons(models.Model):
    """
    Модель иконки категории
    """
    src = models.FileField(upload_to=get_upload_path_by_category, max_length=500, verbose_name=_('icon'))
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='image',
        verbose_name=_('category'),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = _("icon category")
        verbose_name_plural = _("icons categories")

    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        :return: название иконки
        """
        return self.category.title

    def __str__(self):
        return f'{self.pk} icon'