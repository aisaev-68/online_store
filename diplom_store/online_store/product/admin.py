from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Avg, Count
from django.utils.html import format_html
from product.models import Product, ProductImage, Review, Sale, Manufacturer, Seller, Specification


class ProductImageInline(admin.TabularInline):
    model = ProductImage

# class RatingInline(admin.TabularInline):
#     model = Rating


class ReviewInline(admin.TabularInline):
    model = Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'count', 'date', 'available', 'rating_info', 'reviews_list')
    list_filter = ('category', 'available')
    search_fields = ('title',)
    inlines = [ProductImageInline, ReviewInline]



    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'price', 'count', 'available')
        }),
        ('Дополнительная информация', {
            'fields': ('fullDescription', 'freeDelivery', 'limited', 'banner', 'brand', 'seller', 'attributes', 'tags')
        }),

    )
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(rating=Avg('rating_info'), reviews=Count('reviews'))
    #     return queryset



# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'image', 'product']
#     list_filter = ['product']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'city', 'address']
    list_filter = ['name', 'address']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_filter = ['name',]

# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'rating', 'count']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'date', 'rate']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count', 'salePrice', 'dateFrom', 'dateTo']
    list_filter = ['dateFrom', 'dateTo']


