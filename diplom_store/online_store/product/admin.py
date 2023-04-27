from django.contrib import admin

from product.models import Product, ProductImage, Tag, Sale, Review


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
    search_fields = ['name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели продуктов, участвующих в распродаже.
    """
    list_display = ['pk', 'product', 'price', 'salePrice']
    list_display_links = ['pk', 'product']
    search_fields = ['product']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели отзывов.
    """
    list_display = ['pk', 'author', 'email', 'text', 'date', 'product']
    list_display_links = ['pk', 'author']
    search_fields = ['author', 'text']