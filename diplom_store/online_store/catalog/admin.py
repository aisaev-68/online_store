from django.contrib import admin

from catalog.models import Catalog, CatalogIcons, Category, CategoryIcons


@admin.register(Catalog)
class CatalogyAdmin(admin.ModelAdmin):
    """
    Отображение каталогов в административной панели
    """
    list_display = ['pk', 'title']
    list_display_links = ['pk', 'title']


@admin.register(CatalogIcons)
class CatalogyIconsAdmin(admin.ModelAdmin):
    """
    Отображение каталогов в административной панели
    """
    list_display = ['pk', 'src', 'catalog']
    list_display_links = ['pk', 'src']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ['pk', 'title', 'catalog']
    list_display_links = ['pk', 'title']


@admin.register(CategoryIcons)
class CategoryIconsAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ['pk', 'src', 'category']
    list_display_links = ['pk', 'src']