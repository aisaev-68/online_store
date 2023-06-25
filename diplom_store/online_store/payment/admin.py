from django.contrib import admin
from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'month', 'year')
    search_fields = ('number', 'name')
