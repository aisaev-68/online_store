
from django.contrib import admin
from django import forms
from django.db import models

from online_store import settings
from order.models import Order

from product.models import Product


class ProductItemInline(admin.TabularInline):
    model = Order.products.through
    extra = 0

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'deliveryType': forms.Select(choices=settings.SHIPPING_METHODS),
            'paymentType': forms.Select(choices=settings.PAYMENT_METHODS),
            'status': forms.Select(choices=settings.ORDER_STATUSES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['deliveryType'] = instance.deliveryType
            self.initial['paymentType'] = instance.paymentType
            self.initial['status'] = instance.status

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'fullName', 'deliveryType', 'status')
    fieldsets = (
        ('General', {
            'fields': ('user', 'fullName', 'deliveryType', 'status')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Delivery Details', {
            'fields': ('city', 'address')
        }),
        ('Payment', {
            'fields': ('paymentType', 'totalCost', 'payment')
        }),
    )



    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'deliveryType':
            kwargs['choices'] = settings.SHIPPING_METHODS
        elif db_field.name == 'paymentType':
            kwargs['choices'] = settings.PAYMENT_METHODS
        elif db_field.name == 'status':
            kwargs['choices'] = settings.ORDER_STATUSES
        return super().formfield_for_dbfield(db_field, **kwargs)