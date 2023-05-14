from django.contrib import admin

from catalog.models import Catalog, Category, CategoryIcons, CatalogIcons


class CatalogIconsInline(admin.StackedInline):

    model = CatalogIcons
    can_delete = False


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    """
    Отображение каталогов в административной панели
    """
    inlines = [CatalogIconsInline]


class CategoryIconsInline(admin.StackedInline):
    model = CategoryIcons
    can_delete = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    inlines = [CategoryIconsInline]