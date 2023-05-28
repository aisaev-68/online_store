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


class Category(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=100, db_index=True, verbose_name=_('category'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    src = models.ImageField(upload_to=get_upload_path_by_category, null=True, blank=True)


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

    def alt(self):
        return self.title

    def __str__(self):
        return self.title