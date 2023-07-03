from rest_framework import generics
from rest_framework.filters import BaseFilterBackend

from product.models import Product


# page=1&sort=price&sortType=inc&
# filter[name]=&
# filter[minPrice]=0&
# filter[maxPrice]=50000&
# filter[freeDelivery]=false&
# filter[available]=true&limit=20

class ProductFilterSet(BaseFilterBackend):
    @staticmethod
    def filter_queryset(self, request, queryset, view):
        # Извлечение параметров запроса

        sort = request.query_params.get('sort')
        sort_type = request.query_params.get('sortType')
        name_filter = request.query_params.get('filter[name]')
        min_price = request.query_params.get('filter[minPrice]')
        max_price = request.query_params.get('filter[maxPrice]')
        free_delivery = request.query_params.get('filter[freeDelivery]')
        available = request.query_params.get('filter[available]')

        # Применение фильтров к queryset
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if free_delivery:
            queryset = queryset.filter(free_delivery=free_delivery.lower() == 'true')
        if available:
            queryset = queryset.filter(available=available.lower() == 'true')
        if sort:
            sort_field = '-' + sort if sort_type == 'desc' else sort
            queryset = queryset.order_by(sort_field)

        # Возвращение отфильтрованного queryset
        return queryset
