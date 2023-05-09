import random

from django.core.paginator import Paginator
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category

from product.serializers import ProductSerializer


class CategoryView(View):
    """
    Представление для получения категорий товаров
    """

    def get(self, request):
        pass

class CatalogView(View):
    """
    Представление для получения товаров каталога
    """

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class BannersView(View):
    """
    Представление для получения баннеров главной страницы
    """

    def get(self, request):
        pass


class TagsView(View):
    """
    Представление для получения тэгов товаров
    """

    def get(self, request):
        pass

