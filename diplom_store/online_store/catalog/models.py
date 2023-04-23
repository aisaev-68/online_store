from django.db import models

def category_image_directory_path(instance: 'CategoryIcons', filename):
    """
    Получение пути для загрузки иконки категории
    :param instance: экземпляр класса
    :param filename: имя загружаемого файла
    :return: путь для загрузки файла
    """
    if instance.category.parent:
        return f'catalog/icons/{instance.category.parent}/{instance.category}/{filename}'
    else:
        return f'catalog/icons/{instance.category}/{filename}'


class Category(models.Model):
    title = models.TextField(max_length=50, verbose_name='название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class CategoryIcons(models.Model):
    """
    Модель иконки категории
    """
    src = models.FileField(upload_to=category_image_directory_path, max_length=500, verbose_name='иконка')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='image', verbose_name='категория',
                                    blank=True, null=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "иконка категории"
        verbose_name_plural = "иконки категорий"

    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        :return: название иконки
        """
        return self.category.title

    def __str__(self):
        return f'{self.pk}-иконка'

