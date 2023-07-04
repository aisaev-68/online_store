from datetime import datetime
from django.db.models import F, FloatField, Count, Q, Avg, DecimalField
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, status
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from catalog.models import Category
from catalog.serializers import CategorySerializer
from payment.models import PaymentSettings

from product.models import Product, Sale
from product.serializers import ProductSerializer, SaleSerializer, ProductOrderSerializer


def add_catalog_params(func):
    return swagger_auto_schema(
        operation_description='get catalog items',
        manual_parameters=[
            openapi.Parameter(
                'filterSearch',
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


class CategoryAPIView(APIView):
    """
    Представление для получения категорий товаров.
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: CategorySerializer(many=True)},
        operation_description="get catalog menu",
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CatalogAPIView(APIView):
    permission_classes = (AllowAny,)

    def filter_queryset(self, queryset):
        # Извлечение параметров запроса
        print(555, self.request)
        search_text = self.request.query_params.get('filterSearch')
        print("REARCH_TEXT", search_text)
        category = self.request.query_params.get('category')
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')
        name_filter = self.request.query_params.get('filter[name]')
        min_price = self.request.query_params.get('filter[minPrice]')
        max_price = self.request.query_params.get('filter[maxPrice]')
        sellers_filter = [value for key, value in self.request.query_params.items() if 'filter[sellers]' in key]

        specifications_filter = [{key: value} for key, value in self.request.query_params.items() if
                                 'filter[specifications]' in key]
        print(666666666666, specifications_filter)
        manufacturers_filter = [value for key, value in self.request.query_params.items() if
                                'filter[manufacturers]' in key]
        free_delivery = self.request.query_params.get('filter[freeDelivery]')
        available = self.request.query_params.get('filter[available]')
        tags = self.request.query_params.get('tags[]')
        # Применение фильтров к queryset
        if search_text:
            queryset = queryset.filter(
                Q(title__icontains=search_text) | Q(fullDescription__icontains=search_text)
            )
            if not category:
                category = queryset.first().category_id
        if category:
            queryset = queryset.filter(category_id=category)
        if name_filter:
            queryset = queryset.filter(title__icontains=name_filter)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if len(specifications_filter) > 1:
            # Итерируемся по фильтру и извлекаем атрибуты
            attributes = {}
            for index, item in enumerate(specifications_filter):
                for key, value in item.items():
                    if index % 2 == 0:
                        v = value
                    else:
                        k = key

                    print(key, value)
                    # if not attributes.get(item[key]):
                    #     attributes[item[key]] = [item[value]]
                    # else:
                    #     lst = attributes[item[key]]
                    #     attributes[item[key]] = lst.append(attributes[item[key]])


            print("ATTR", attributes)
            # Создаем список Q-объектов для каждого фильтра
            q_objects = []
            for index, attrs in attributes.items():
                q_object = Q()
                for attr, value in attrs.items():
                    q_object &= Q(attributes__contains={attr + index: value})
                q_objects.append(q_object)
                print("Q_OBJECT", q_objects)
            # Сводим все Q-объекты с использованием оператора AND
            query = Q()
            for q_object in q_objects:
                query &= q_object
            queryset = queryset.filter(query)

        filters_sellers = Q()
        if len(sellers_filter) >= 1:
            for seller in sellers_filter:
                filters_sellers |= Q(seller__name=seller)
            queryset = queryset.filter(filters_sellers)

        filters_manufacturers = Q()
        if len(manufacturers_filter) >= 1:
            for manufacturer in manufacturers_filter:
                filters_manufacturers |= Q(brand__name=manufacturer)
            queryset = queryset.filter(filters_manufacturers)

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
        settings = PaymentSettings.objects.first()
        limit = settings.page_size

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
    def get(self, request: Request, pk: int = None) -> Response:
        print("PK", pk)
        if pk is not None:
            print(999999999)
            queryset = self.filter_queryset(
                Product.objects.filter(category_id=pk, available=True).order_by('-date').all())
        else:
            print(1000000000)
            queryset = self.filter_queryset(Product.objects.filter(available=True).order_by('-date').all())

        data = self.pagination_queryset(queryset)
        paginated_queryset = data['pagination']
        serialized_data = ProductSerializer(paginated_queryset, many=True).data

        response_data = {
            'items': serialized_data,
            'currentPage': data['currentPage'],
            'lastPage': data['lastPage'],
        }
        print("SEARCH", response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ProductPopularAPIView(APIView):
    """
    Представление для получения популярных продуктов
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        products = Product.objects.annotate(
            sort_index=Cast((1 / F('price')), output_field=FloatField()) + Avg('reviews__rate',
                                                                               filter=Q(reviews__isnull=False)),
        ).order_by('sort_index', '-count')[:8]

        for product in products:
            product.title = product.title[:25] + '...'
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductLimitedAPIView(APIView):
    """
    Представление для получения лимитированных продуктов
    """

    def get(self, request: Request) -> Response:
        products = Product.objects.filter(limited=False).prefetch_related('images').order_by('id')[:16]

        for product in products:
            product.title = product.title[:25] + '...'
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesAPIView(APIView):
    """
    Представление для получения товаров со скидками.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        products = (Sale.objects
                    .filter(Q(dateFrom__gte=datetime.today()) | Q(dateTo__gte=datetime.today()))
                    .select_related('product')
                    .filter(product__available=True)).order_by("salePrice")
        setting = PaymentSettings.objects.first()
        paginator = Paginator(products, setting.page_size)
        current_page = paginator.get_page(request.GET.get('page', 1))
        if len(products) % setting.page_size == 0:
            lastPage = len(products) // setting.page_size
        else:
            lastPage = len(products) // setting.page_size + 1
        serializer = SaleSerializer(current_page, many=True)
        return Response(
            {'salesCards': serializer.data, 'currentPage': request.GET.get('page', 1), 'lastPage': lastPage},
            status=status.HTTP_200_OK)


class BannersAPIView(APIView):
    """
    Представление для получения баннеров главной страницы.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        products = Product.objects.filter(banner=True).prefetch_related('images').order_by('id')[:4]
        serializer = ProductOrderSerializer(products, many=True)
        print("BANNER", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchAPIView(APIView):

    def get(self, request: Request) -> Response:
        search_text = self.request.query_params.get('filterSearch')
        product = Product.objects.filter(title__icontains=search_text).first()
        return Response({'category': product.category_id}, status=status.HTTP_200_OK)
