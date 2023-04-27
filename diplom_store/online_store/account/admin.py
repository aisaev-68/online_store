from django.contrib import admin
from account.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователя в административной панели
    """
    list_display = ['pk', 'username', 'fullName', 'email', 'phone', 'avatar']
    list_filter = ('is_staff', 'is_superuser', 'groups')
    list_display_links = ['fullName', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name','first_name', "surname", 'email', 'phone', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'last_name', 'first_name', "surname", 'email', 'phone', 'avatar', 'password1', 'password2'),
        }),
    )
    def fullName(self, obj: User):
        """
        Полное имя
        """
        return obj.last_name + ' ' + obj.first_name + ' ' + obj.surname

    def passw(self, obj: User):
        return obj.set_password(obj.password)