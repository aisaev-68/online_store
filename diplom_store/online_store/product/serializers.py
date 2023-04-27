import datetime

from rest_framework import serializers
import locale
from product.models import Product, Review, Tag, Sale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')




class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализация отзывов о продукте
    """
    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date',]



class TagSerializer(serializers.ModelSerializer):
    """
    Сериализация тегов продукта
    """
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализация продукта
    """
    id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()
    description = serializers.StringRelatedField()
    tags = TagSerializer(many=True, required=False)
    reviews = ReviewSerializer(many=True, required=False)
    href = serializers.StringRelatedField()
    photoSrc = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'category',
                  'price', 'count',
                  'date', 'title',
                  'description', 'fullDescription',
                  'href', 'freeDelivery',
                  'images', 'tags', 'reviews',
                  'rating']

    def get_photoSrc(self, instance):
        """
        Получение главного изображения продукта
        :return: изображение
        """
        src = [str(instance.images.first())]
        return src

    def get_images(self, instance):
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append(image.__str__())
        return images

    def get_price(self, instance):
        """
        Получение цены продукта в зависимости от наличия скидки
        :return: цена
        """
        salePrice = instance.sales.first()  # Если товар есть в таблице с распродажами, то берем цену из этой таблицы
        if salePrice:
            return salePrice.salePrice
        return instance.price


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