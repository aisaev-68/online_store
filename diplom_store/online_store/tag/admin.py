from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']