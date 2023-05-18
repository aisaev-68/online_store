from django.db import models
from django.utils.translation import gettext_lazy as _



class Tag(models.Model):
    """
    Модель тега
    """
    id = models.CharField(primary_key=True, max_length=50, verbose_name=_('id tag'))
    name = models.CharField(max_length=50, default='', db_index=True, verbose_name=_('name'))



    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


    def __str__(self):
        return self.name
