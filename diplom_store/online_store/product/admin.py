from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils.html import format_html
from product.models import Product, ProductImage, Rating, Review, Sale, Manufacturer, Seller, Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'count', 'date', 'available']
    list_filter = ['category', 'available']
    search_fields = ['title']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product']
    list_filter = ['product']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'city', 'address']
    list_filter = ['name', 'address']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_filter = ['name',]

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'rating', 'count']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'date']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count', 'salePrice', 'dateFrom', 'dateTo']
    list_filter = ['dateFrom', 'dateTo']


