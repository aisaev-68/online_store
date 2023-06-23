
from django.contrib import admin
from django.utils import timezone
from django import forms
from django.db import models

from online_store import settings
from order.models import Order

from product.models import Product

from payment.models import Payment

from order.models import OrderProducts

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'month', 'year')
    search_fields = ('number', 'name')


class PaymentInline(admin.StackedInline):
    model = Order
    can_delete = False
    fields = ('payment_number', 'payment_name', 'payment_month', 'payment_year', 'payment_code')


class OrderProductsInline(admin.TabularInline):
    model = OrderProducts
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'fullName', 'deliveryType', 'createdAt', 'status')
    list_filter = ('status', 'deliveryType')
    search_fields = ('orderId', 'fullName', 'email', 'phone')
    inlines = [OrderProductsInline, PaymentInline]

    fieldsets = (
        ('General', {
            'fields': ('orderId', 'user', 'fullName', 'email', 'phone')
        }),
        ('Delivery', {
            'fields': ('deliveryType', 'city', 'address')
        }),
        ('Payment', {
            'fields': ('paymentType', 'totalCost')
        }),
        # ('Payment Details', {
        #     'fields': ('payment_number', 'payment_name', 'payment_month', 'payment_year', 'payment_code'),
        #     'classes': ('collapse',),
        # }),
        ('Status', {
            'fields': ('status',),
        }),
    )

    ordering = ('-createdAt',)
    readonly_fields = ('orderId',)

    def save_model(self, request, obj, form, change):
        if not change:
            # При создании нового заказа, установите поле created_at
            obj.created_at = timezone.now()
        super().save_model(request, obj, form, change)


    def payment_number(self, obj):
        return obj.payment.number

    def payment_name(self, obj):
        return obj.payment.name

    def payment_month(self, obj):
        return obj.payment.month

    def payment_year(self, obj):
        return obj.payment.year

    def payment_code(self, obj):
        return obj.payment.code
    #
    payment_number.short_description = 'Payment Number'
    payment_name.short_description = 'Payment Name'
    payment_month.short_description = 'Payment Month'
    payment_year.short_description = 'Payment Year'
    payment_code.short_description = 'Payment Code'
