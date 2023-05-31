import datetime

from rest_framework import serializers
import locale
from product.models import Product, Review, Sale, ProductImage, Rating, Seller, Manufacturer, Specification
from tag.serializers import TagSerializer

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = ('author', 'email', 'text', 'date')
        fields = ('id',)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'count')

class CurrentLastPageSerializer(serializers.Serializer):
    current_page = serializers.SerializerMethodField()
    last_page = serializers.SerializerMethodField()

    def get_current_page(self, obj):
        request = self.context['request']
        if request is not None:
            return int(request.query_params.get('page', 1))
        return None

    def get_last_page(self, obj):
        paginator = self.context['view'].paginator
        if paginator is not None:
            return paginator.num_pages
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='rating_info.rating')
    reviews = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'href', 'freeDelivery',
                  'images', 'tags', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_count(self, obj):
        return obj.rating_info.count

    def get_images(self, obj):
        return ['/media/' + str(image.image) for image in obj.images.all()]

    def get_href(self, obj):
        return obj.href()

    def get_description(self, obj):
        if len(obj.fullDescription) > 50:
            return f'{obj.fullDescription[:50]}...'
        return obj.fullDescription

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериализация товаров со скидками
    """
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.product.price
    def get_images(self, obj):
        product_images = obj.product.images.all()
        return [image.src() for image in product_images]

    def get_href(self, obj):
        return f'/product/{obj.product.pk}'

    class Meta:
        model = Sale
        fields = ('id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'href', 'images')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('pk', 'name',)


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('pk', 'name', 'city', 'address')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ('id', 'attributes')