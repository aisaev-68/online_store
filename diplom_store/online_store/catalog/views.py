import random
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters, pagination
from rest_framework.pagination import PageNumberPagination
from catalog.filters import ProductFilterSet
from catalog.models import Category, Catalog
from catalog.serializers import CatalogSerializer

from product.models import Product, Sale
from product.serializers import ProductSerializer, SaleSerializer, CurrentLastPageSerializer


class CategoryView(APIView):
    """
    Представление для получения категорий товаров.
    """

    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)


class CatalogView(APIView):

    def filter_queryset(self, queryset):
        # Извлечение параметров запроса
        print(44444, self.request.query_params)
        if self.request.query_params.get('category'):
            category = self.request.query_params.get('category')
        else:
            category = self.kwargs.get('id')
        # category = self.request.query_params.get('category')
        # print(111, category)
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')
        name_filter = self.request.query_params.get('filter[name]')
        min_price = self.request.query_params.get('filter[minPrice]')
        max_price = self.request.query_params.get('filter[maxPrice]')
        free_delivery = self.request.query_params.get('filter[freeDelivery]')
        available = self.request.query_params.get('filter[available]')

        # Применение фильтров к queryset
        if category:
            queryset = queryset.filter(category_id=category)
        if name_filter:
            queryset = queryset.filter(title__icontains=name_filter)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if free_delivery:
            queryset = queryset.filter(freeDelivery=free_delivery.lower() == 'true')
        if available:
            queryset = queryset.filter(available=available.lower() == 'true')
        if sort:
            sort_field = '-' + sort if sort_type == 'dec' else sort
            print("SORT_TYPE", sort_type)
            print("CURRENT_SORT ", sort_field)
            queryset = queryset.order_by(sort_field)

        return queryset

    def get(self, request):
        queryset = self.filter_queryset(Product.objects.all())
        len_products = len(queryset)
        serializer = ProductSerializer(queryset, many=True)

        paginator = PageNumberPagination()
        limit = int(request.GET.get('limit', 8))
        paginator.page_size = limit
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = ProductSerializer(paginated_queryset, many=True).data

        current_page = int(request.GET.get('page', 1))
        last_page = len_products // limit + 1

        response_data = {
            'items': serialized_data,
            'currentPage': current_page,
            'lastPage': last_page,
        }

        return Response(response_data)




class CatalogByIdView(APIView):
    """
    Представление для получения каталога по ID.
    """

    def get(self, request, id):
        products = Product.objects.filter(category_id=id).all()
        serializer = ProductSerializer(products, many=True)
        print(88888, serializer.data)
        context = {
                'items': serializer.data,
                'currentPage': 5,
                'lastPage': 10
            }
        # return Response(data=context, template_name='frontend/catalog.html')
        return render(request, 'frontend/catalog.html', context=context)


class ProductPopularView(View):
    """
    Представление для получения популярных продуктов
    """
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category_id=self.kwargs['id']).prefetch_related('images')
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
