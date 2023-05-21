
from django.contrib import admin

from order.models import Order

from product.models import Product


class ProductItemInline(admin.TabularInline):
    model = Product
    extra = 5


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # inlines = [
    #     ProductItemInline,
    # ]
    list_display = ('user',
                    'products',
                    'createdAt',
                    'deliveryType',
                    'paymentType',
                    'status',
                    'city',
                    'address',
                    'totalCost')
    list_filter = ('createdAt', 'deliveryType', 'paymentType', 'status', 'city')
    search_fields = ('user__username', 'products__title', 'city', 'address')
    date_hierarchy = 'createdAt'
    ordering = ('-createdAt',)
