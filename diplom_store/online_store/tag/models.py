from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product


class Tag(models.Model):
    """
    Модель тега
    """
    name = models.CharField(max_length=128, default='', db_index=True, verbose_name=_('name'))
    product = models.ManyToManyField(Product, related_name='tags', verbose_name=_('tag'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


    def __str__(self):
        return self.name