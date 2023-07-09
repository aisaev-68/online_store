from django.contrib import admin

from settings.models import PaymentSettings


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели
    """
    list_display = ('payment_methods', 'shipping_methods', 'order_status', 'page_size')