from django.contrib import admin

from catalog.models import Catalog, Category


@admin.register(Catalog)
class CatalogyAdmin(admin.ModelAdmin):
    """
    Отображение каталогов в административной панели
    """
    list_display = ['pk', 'title', 'src']
    list_display_links = ['pk', 'title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ['pk', 'title', 'src', 'catalog']
    list_display_links = ['pk', 'title']