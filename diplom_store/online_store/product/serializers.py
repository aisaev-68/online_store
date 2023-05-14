import datetime

from rest_framework import serializers
import locale
from product.models import Product, Review, Sale, ProductImage, Rating


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'date')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'count')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    count = serializers.IntegerField(source='count')  # Просто чтобы показать, как использовать source

    class Meta:
        model = Product
        fields = (
        'id', 'category', 'price', 'count', 'date', 'title', 'description', 'href', 'freeDelivery', 'images', 'tags',
        'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        rating_info = obj.rating_info()
        return rating_info['rating']

    def get_href(self, obj):
        return obj.href()

    def get_description(self, obj):
        return obj.description()


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериализация товаров со скидками
    """
    images = serializers.StringRelatedField(many=True)
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    dateFrom = serializers.DateField(format='%d.%b')
    dateTo = serializers.DateField(format='%d.%b')

    class Meta:
        model = Sale
        fields = '__all__'
