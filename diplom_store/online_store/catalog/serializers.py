from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from catalog.models import Category
from product.models import Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    """
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'href', 'subcategories']

    def get_image(self, obj):
        return {
            'src': obj.src.url if obj.src else '',
            'alt': obj.title
        }

    def get_subcategories(self, obj):
        subcategories = obj.children.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return serializer.data


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор подкатегорий товара.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'href']

    def get_image(self, obj):
        return {
            'src': obj.src.url if obj.src else '',
            'alt': obj.title
        }


class BannersSerializer(serializers.ModelSerializer):
    """
    Сериализация баннеров для главной страницы (категорий товаров)
    """
    price = serializers.StringRelatedField()
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['title', 'href', 'price', 'images']
