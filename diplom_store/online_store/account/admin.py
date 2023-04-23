from django.contrib import admin
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователя в административной панели
    """
    list_display = ['pk', 'username', 'email', 'fullName', 'phone', 'avatar', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'password']
    list_display_links = ['fullName', 'email']
