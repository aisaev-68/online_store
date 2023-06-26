
from django.contrib import admin
from django.utils import timezone

from order.models import Order

from payment.models import Payment

from order.models import OrderProducts




class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False
    fields = ('number', 'name', 'month', 'year', 'code')


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



