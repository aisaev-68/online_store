import random

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category
from catalog.serializers import BannersSerializer, TagsSerializer, CategorySerializer
from product.models import Tag
from product.serializers import ProductSerializer


class CategoryView(APIView):
    """
    Представление для получения категорий товаров
    """

    def get(self, request):
        categories = []
        categories_tmp = Category.objects.filter(parent=None, active=True).prefetch_related('image', 'subcategories')
        for category in categories_tmp:
            subcategories = [subcategory for subcategory in category.subcategories.filter(active=True)]
            categories.append({'id': category.id, 'title': category.title, 'subcategories': subcategories,
                               'href': category.href, 'image': category.image})
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CatalogView(APIView):
    """
    Представление для получения товаров каталога
    """

    def get(self, request, *args, **kwargs):
        pass
        # products = filter_catalog(request)
        # products = sorting_catalog(request, products)
        # paginator = Paginator(products, 8)
        # current_page = paginator.get_page(request.GET.get('page'))
        # if len(products) % 8 == 0:  # Определяем количество страниц для отображения на сайте
        #     lastPage = len(products) // 8
        # else:
        #     lastPage = len(products) // 8 + 1
        # for product in current_page:
        #     product.categoryName = product.category
        # serializer = ProductSerializer(current_page, many=True)
        # return Response({'items': serializer.data, 'currentPage': request.GET.get('page'), 'lastPage': lastPage})

    def post(self, request, *args, **kwargs):
        pass


class BannersView(APIView):
    """
    Представление для получения баннеров главной страницы
    """

    def get(self, request):
        categories = []
        categories_tmp = Category.objects.filter(parent__isnull=False, active=True, favourite=True).prefetch_related(
            'products')
        if len(categories_tmp) > 3:
            categories_tmp = random.sample(list(categories_tmp), 3)
        for category in categories_tmp:
            product = category.products.order_by('price').first()
            product_min_price = product.price
            product_image = product.images
            categories.append({'href': category.href, 'title': category.title, 'price': product_min_price,
                               'images': product_image})
        serializer = BannersSerializer(categories, many=True)
        return Response({'banners': serializer.data})


class TagsView(APIView):
    """
    Представление для получения тэгов товаров
    """

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)


