from rest_framework import serializers
import locale

from product.models import Product, Review, Sale, ProductImage, Seller, Manufacturer, Specification


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ReviewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'date', 'rate')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["date"] = obj.date.strftime('%Y-%m-%d %H:%M')
        return data

class ProductReviewsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    description = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription', 'href', 'freeDelivery',
                  'images', 'tags', 'specifications', 'reviews', 'rating')

    def get_specifications(self, obj):
        return obj.attributes

    def get_rating(self, obj):
        return obj.rating_info()

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
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription', 'href', 'freeDelivery',
                  'images', 'tags', 'attributes', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        return obj.rating_info()

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

    def get_title(self, obj):
        return obj.title[:25]

class ProductOrderSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='rating_info')

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'href',
                  'freeDelivery', 'images', 'tags', 'reviews', 'rating')

    def get_title(self, obj):
        return obj.title[:25]

    def get_images(self, instance):
        images = instance.images.all()
        image_urls = [image.image.url for image in images]
        return image_urls

    def get_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]

    def get_reviews(self, instance):
        return instance.reviews.count()

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


    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["dateFrom"] = obj.dateFrom.strftime('%d.%m')
        data["dateTo"] = obj.dateTo.strftime('%d.%m')
        return data


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
