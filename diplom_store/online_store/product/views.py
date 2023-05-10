from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Review, Sale
from product.serializers import ProductSerializer, ReviewSerializer, SaleSerializer


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'frontend/index.html')


class ProductCatalogView(View):
    """
        Представление для отображения популярных продуктов
    """
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category=self.kwargs['category']).prefetch_related('images')
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = 1
        paginator = Paginator(products, 6)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, 'product/catalog.html', context={"page": results})

class ProductPopularView(View):
    """
        Представление для отображения популярных продуктов
    """
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category=self.kwargs['category']).prefetch_related('images')
        return render(request, 'product/catalog.html', context={'products': products[:6]})


class ProductLimitedView(APIView):
    """
    Представление для отображения лимитированных продуктов
    """

    def get(self, request):
        products = Product.objects.prefetch_related('images')
        for product in products:
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class FilterProduct(View):
    def get(self, request, min_price=None, max_price=None, in_stock=None, free_shipping=None, *args, **kwargs):
        # Получаем все товары
        products = Product.objects.all()

        # Применяем фильтры
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if in_stock is not None:
            products = products.filter(in_stock=in_stock)
        if free_shipping is not None:
            products = products.filter(freeDelivery=free_shipping)

        return products


class SalesView(APIView):
    """
    Представление для отображения товаров со скидками.
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


class BannerView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class ProductDetailView(viewsets.ViewSet):
    """
    Представление для отображения детальной страницы продукта
    """

    def retrieve(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class ProductReviewView(CreateModelMixin, GenericAPIView):
    """
    Представление для создания отзывов о продукте
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.create()
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        pk = kwargs['pk']
        request.data['product'] = pk
        request.data['date'] = datetime.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        reviews = Review.objects.filter(product=pk)
        serializer = self.serializer_class(reviews, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



