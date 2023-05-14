import random
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category, Catalog
from catalog.serializers import CatalogSerializer

from product.models import Product, Sale
from product.serializers import ProductSerializer, SaleSerializer


class CategoryView(APIView):
    """
    Представление для получения категорий товаров.
    """

    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)


class CatalogView(APIView):
    """
    Представление для получения товаров каталога.
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


class CatalogByIdView(APIView):
    """
    Представление для получения каталога по ID.
    """

    def get(self, request, *args, **kwargs):
        pass

class ProductPopularView(View):
    """
    Представление для получения популярных продуктов
    """
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category=self.kwargs['category']).prefetch_related('images')
        return render(request, 'product/catalog.html', context={'products': products[:6]})


class ProductLimitedView(APIView):
    """
    Представление для получения лимитированных продуктов
    """

    def get(self, request):
        products = Product.objects.prefetch_related('images')
        for product in products:
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class SalesView(APIView):
    """
    Представление для получения товаров со скидками.
    """
    def get(self, request, *args, **kwargs):
        count_products_on_page = 8  # Определяем количество продуктов на странице
        products = (Sale.objects.filter(Q(dateFrom__gte=datetime.today()) | Q(dateTo__gte=datetime.today())).
                    select_related('product').filter(product__active=True))
        paginator = Paginator(products, 8)
        current_page = paginator.get_page(request.GET.get('page'))
        if len(products) % count_products_on_page == 0:
            lastPage = len(products) // count_products_on_page
        else:
            lastPage = len(products) // count_products_on_page + 1
        serializer = SaleSerializer(current_page, many=True)
        return Response({'salesCards': serializer.data, 'currentPage': request.GET.get('page'), 'lastPage': lastPage})


class BannersView(View):
    """
    Представление для получения баннеров главной страницы.
    """

    def get(self, request, *args, **kwargs):
        pass
