from django.contrib import admin

from catalog.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ('title', 'parent')
    list_filter = ('title',)
    ordering = ('title', 'pk')