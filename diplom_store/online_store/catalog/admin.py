from django.contrib import admin

from catalog.models import Category
from product.models import Specification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ('title', 'parent')
    list_filter = ('title',)
    ordering = ('title', 'pk')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'attributes', 'category']
    list_filter = ['category',]