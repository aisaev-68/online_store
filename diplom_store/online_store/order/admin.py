
from django.contrib import admin

from order.models import Order

from product.models import Product


class ProductItemInline(admin.TabularInline):
    model = Order.products.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductItemInline,
    ]
    list_display = ('user',
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
    # fieldsets = (
    #     (_('Информация о покупателе'), {
    #         'classes': ('collapse', 'wide'),
    #         'fields': ('user', 'fullname', 'email', 'phone'),
    #     }),
    #     (_('Информация о заказе'), {
    #         'classes': ('collapse', 'wide'),
    #         'fields': ('status', 'city', 'address')
    #     }),
    #     (_('Оплата и доставка'), {
    #         'classes': ('collapse', 'wide'),
    #         'fields': ('totalCost', 'deliveryCost', 'freeDelivery', 'deliveryType', 'paymentType')
    #     }),
    # )