import random

from django.core.paginator import Paginator
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category, Catalog
from catalog.serializers import CatalogSerializer

from product.models import Product
from product.serializers import ProductSerializer

class CategoryView(APIView):
    """
    Представление для получения категорий товаров
    """
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)


class CatalogView(APIView):
    """
    Представление для получения товаров каталога
    """

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                'items': serializer.data,
                'currentPage': 5,
                'lastPage': 10
            }
        )


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

