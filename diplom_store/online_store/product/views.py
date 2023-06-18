from datetime import datetime
from rest_framework.authentication import SessionAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Review, Manufacturer, Seller, Specification
from product.serializers import ProductSerializer, ReviewSerializer, ManufacturerSerializer, SellerSerializer, \
    SpecificationSerializer


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


class FilterAndSort(View):
    template_name = 'product/catalog.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category=self.kwargs['category']).prefetch_related('images')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction', 'asc')
        # Фильтрация по цене
        price_min = request.GET.get('minPrice')
        price_max = request.GET.get('maxPrice')
        if price_min and price_max:
            queryset = queryset.filter(price__range=(price_min, price_max))

        # Фильтрация по названию
        title = request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Фильтрация по бесплатной доставке
        free_delivery = request.GET.get('free_delivery')
        if free_delivery:
            queryset = queryset.filter(freeDelivery=True)

        # Фильтрация по наличию на складе
        in_stock = request.GET.get('in_stock')
        if in_stock:
            queryset = queryset.filter(in_stock=True)

        if order_by == 'price':

            if direction == 'asc':
                queryset = queryset.order_by('price')
            else:
                queryset = queryset.order_by('-price')
        # elif order_by == 'reviews':
        #     queryset = queryset.order_by(
        #         '-reviews')  # Предположим, что у модели Product есть поле 'reviews' для отзывов
        elif order_by == 'newest':
            queryset = queryset.order_by('-date')

        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = 1
        paginator = Paginator(queryset, 6)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        context = {
            'page': results,
            'price_min': price_min,
            'price_max': price_max,
            'title': title,
            'free_delivery': free_delivery,
            'in_stock': in_stock,
        }

        return render(request, self.template_name, context)








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


class SortedPrice(View):
    def get(self, request, *args, **kwargs):
        # Пример сортировки по возрастанию цены
        sorted_products = Product.objects.order_by('price')

        # Пример сортировки по убыванию цены
        sorted_products = Product.objects.order_by('-price')




class BannerView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class ProductDetailView(APIView):
    """
    Представление для получения детальной страницы продукта
    """

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        print("PRODUCT", serializer.data)
        return Response(serializer.data)


class ProductReviewView(APIView):
    """
    Представление для создания отзывов о продукте
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, pk, *args, **kwargs):
        data = request.data
        review = Review.objects.create(authotr='', email='', text='', data=datetime.now(), product=pk)
        serializer = self.serializer_class(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ManufacturerListAPIView(APIView):
    """
    Представление для получения производителей.
    """
    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        print(7777777, manufacturers)
        serializer = ManufacturerSerializer(manufacturers, many=True)
        print(serializer)
        return Response(serializer.data)


class SellerListAPIView(APIView):
    """
    Предсталение для получения продавцов.
    """
    def get(self, request):
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)

        return Response(serializer.data)

class SpecificationAPIView(APIView):
    """
    Представление для получения спецификаций.
    """
    def get(self, request, pk):
        # id = self.request.query_params.get("category")
        specifications = Specification.objects.filter(category=pk).first()
        serializer = SpecificationSerializer(specifications)
        print(888, serializer.data)
        return Response(serializer.data)