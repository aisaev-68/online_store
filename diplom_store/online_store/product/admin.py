from django.contrib import admin

from product.models import Product, ProductImage, Tag, Specification, Sale, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ['pk', 'title', 'image']
    list_display_links = ['pk', 'title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Отображение продуктов в административной панели
    """
    list_display = [
        'pk',
        'title',
        'price',
        'count',
        'category',
        'date',
        # 'freeDelivery',
    ]
    list_display_links = ['pk', 'title']
    list_filter = ['freeDelivery', 'rating']
    search_fields = ['title', 'category', 'price']

    fieldsets = (
        ('О продукте', {
            'fields': ('category', 'title', ('price', 'count', 'rating'))
        }),
        ('Дополнительные параметры', {
            'classes': ('collapse',),
            'fields': ('freeDelivery',)
        }),
        ('Описание товара', {
            'classes': ('collapse',),
            'fields': ('fullDescription',),
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели изображений продуктов
    """
    list_display = ['pk', 'product', 'image']
    list_display_links = ['pk', 'product']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Отображение тегов в административной панели
    """
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели характеристик продуктов
    """
    list_display = ['pk', 'name', 'value']
    list_display_links = ['pk', 'name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели продуктов, участвующих в распродаже
    """
    list_display = ['pk', 'product', 'price', 'salePrice']
    list_display_links = ['pk', 'product']
