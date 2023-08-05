from decimal import Decimal
from rest_framework import serializers

from product.models import Product


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализация корзины продуктов
    """
    count = serializers.SerializerMethodField()
    # price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    href = serializers.StringRelatedField()
    description = serializers.StringRelatedField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.DecimalField(decimal_places=1, max_digits=2, source='rating_info')

    class Meta:
        model = Product
        fields = (
            "id", "category", "price",
            "count", "date", "title",
            "description", "href",
            "freeDelivery", "images",
            "tags", "reviews", "rating"
        )

    def get_count(self, obj):
        # return self.context.get(str(obj.pk)).get('quantity')
        cart = self.context.get('cart', {})
        return cart.get(str(obj.pk), {}).get('quantity', 0)

    def get_price(self, obj):
        return Decimal(self.context.get(str(obj.pk)).get('price'))

    def get_images(self, obj):
        return ['/media/' + str(image.image) for image in obj.images.all()]

    def get_reviews(self, obj):
        return obj.reviews.count()
