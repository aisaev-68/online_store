from datetime import datetime
from django.db.models import F, FloatField, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from catalog.models import Category, Catalog
from catalog.serializers import CatalogSerializer

from product.models import Product, Sale
from product.serializers import ProductSerializer, SaleSerializer


def add_catalog_params(func):
    return swagger_auto_schema(
        operation_description='get catalog items',
        manual_parameters=[
            openapi.Parameter(
                'filter',
                openapi.IN_QUERY,
                description='Search text',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description='Page number',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description='Category ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description='Sort field',
                type=openapi.TYPE_STRING,
                enum=['date', 'price', 'rating', 'reviews']  # Здесь указываем доступные значения
            ),
            openapi.Parameter(
                'sortType',
                openapi.IN_QUERY,
                description='Sort type (dec/inc)',
                type=openapi.TYPE_STRING,
                enum=['dec', 'inc']
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description='Items per page',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )(func)


class CategoryView(APIView):
    """
    Представление для получения категорий товаров.
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: CatalogSerializer},
        operation_description="get catalog menu",
    )
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        # catalogs = Catalog.objects.filter(
        #     subcategories__active=True
        # ).annotate(num_categories=Count(
        #     'subcategories')
        # ).filter(num_categories__gt=0)
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)


class CatalogView(APIView):
    permission_classes = (AllowAny,)

    def filter_queryset(self, queryset):
        # Извлечение параметров запроса

        if self.request.query_params.get('category'):
            category = self.request.query_params.get('category')
        else:
            category = self.kwargs.get('id')
        print('CATEGORY', self.request.query_params.get('category'))
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')
        name_filter = self.request.query_params.get('filter[name]')
        min_price = self.request.query_params.get('filter[minPrice]')
        max_price = self.request.query_params.get('filter[maxPrice]')
        free_delivery = self.request.query_params.get('filter[freeDelivery]')
        available = self.request.query_params.get('filter[available]')
        tags = self.request.query_params.get('tags[]')
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
        if tags:
            queryset = queryset.filter(tags=tags)
        if sort:
            sort_field = '-' + sort if sort_type == 'dec' else sort
            queryset = queryset.order_by(sort_field)

        return queryset
    
    def pagination_queryset(self, queryset):
        len_products = len(queryset)
        paginator = PageNumberPagination()
        limit = int(self.request.GET.get('limit', 8))

        paginator.page_size = limit
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        current_page = int(self.request.GET.get('page', 1))
        if len_products % limit == 0:
            last_page = len_products // limit
        else:
            last_page = len_products // limit + 1

        return {
            'pagination': paginated_queryset,
            'currentPage': current_page,
            'lastPage': last_page,
        }

    @add_catalog_params
    def get(self, request):
        print('CATEGORY9', self.args)
        queryset = self.filter_queryset(Product.objects.all())
        data = self.pagination_queryset(queryset)
        paginated_queryset = data['pagination']
        serialized_data = ProductSerializer(paginated_queryset, many=True).data

        response_data = {
            'items': serialized_data,
            'currentPage': data['currentPage'],
            'lastPage': data['lastPage'],
        }

        return Response(response_data)


class CatalogByIdView(CatalogView):
    """
    Представление для получения каталога по ID.
    """

    @add_catalog_params
    def get(self, request, id: int):
        response = super().get(request)
        print(7777, response)
        if id is not None:
            queryset = Product.objects.filter(category_id=id).all()
            data = self.pagination_queryset(queryset)
            paginated_queryset = data['pagination']
            serialized_data = ProductSerializer(paginated_queryset, many=True).data

            response_data = {
                'items': serialized_data,
                'currentPage': data['currentPage'],
                'lastPage': data['lastPage'],
            }
            return Response(response_data)


class ProductPopularView(APIView):
    """
    Представление для получения популярных продуктов
    """

    def get(self, request, *args, **kwargs):
        products = Product.objects.annotate(
            sort_index=(1 / F('price')) + F('rating_info__rating'),
        ).order_by('sort_index', '-count')[:8]
        for product in products:
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class ProductLimitedView(APIView):
    """
    Представление для получения лимитированных продуктов
    """

    def get(self, request):
        products = Product.objects.filter(limited=False).prefetch_related('images').order_by('id')[:16]

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
