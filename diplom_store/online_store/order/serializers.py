import datetime

from rest_framework import serializers
from order.models import Order, OrderProducts
from product.serializers import ProductSerializer, ProductOrderSerializer

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализация заказа
    """
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', )

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['orderId'] = obj.pk
        data['fullName'] = obj.user.fullName
        data['email'] = obj.user.email
        data['phone'] = obj.user.phone
        data['createdAt'] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        return data

class OrderProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = OrderProducts
        fields = ('products',)

    def get_products(self, instance):
        product_serializer = ProductOrderSerializer(instance.product)
        serialized_product = product_serializer.data
        serialized_product['count'] = instance.count_product

        return serialized_product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['products']

class OrderProductSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(source='orderproducts_set.all', many=True)

    class Meta:
        model = Order
        fields = ('orderId', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address', 'products')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["createdAt"] = obj.createdAt.strftime('%Y-%m-%d %H:%M')
        return data