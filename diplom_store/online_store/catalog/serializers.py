from rest_framework import serializers

from catalog.models import Catalog, CatalogIcons, Category, CategoryIcons
# from product.models import Tag


class CategoryIconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryIcons
        fields = ('src', 'alt')


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryIconsSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'href')


class CatalogIconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogIcons
        fields = ('src', 'alt')


class CatalogSerializer(serializers.ModelSerializer):
    image = CatalogIconsSerializer(read_only=True)
    subcategories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'title', 'image', 'href', 'subcategories')



# class TagsSerializer(serializers.ModelSerializer):
#     """
#     Сериализация тегов товара
#     """
#
#     class Meta:
#         model = Tag
#         exclude = ['product']


class BannersSerializer(serializers.ModelSerializer):
    """
    Сериализация баннеров для главной страницы (категорий товаров)
    """
    price = serializers.StringRelatedField()
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ['title', 'href', 'price', 'images']


