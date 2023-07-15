import logging
from datetime import datetime
from rest_framework.authentication import SessionAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from product.models import Product, Review, Manufacturer, Seller, Specification
from product.serializers import ReviewSerializer, ManufacturerSerializer, SellerSerializer, \
    SpecificationSerializer, ProductReviewsSerializer

logger = logging.getLogger(__name__)

class MainPageView(View):
    """
    Представление для перехода на главную страницу.
    """
    def get(self, request, *args, **kwargs):
        logger.info(_('Go to home page'))
        return render(request, 'frontend/index.html')


class ProductDetailView(APIView):
    """
    Представление для получения детальной страницы продукта
    """

    @swagger_auto_schema(
        responses={200: ProductReviewsSerializer(many=False)},
        operation_description="get product detail",
    )
    def get(self, request, pk) -> Response:
        product = Product.objects.prefetch_related('reviews').get(pk=pk)
        product.title = product.title[:50]
        serializer = ProductReviewsSerializer(product, many=False)
        logger.info(_('Getting detailed information about a product № %s'), product.id)
        print(666666666, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewView(APIView):
    """
    Представление для создания отзывов о продукте
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'text': openapi.Schema(type=openapi.TYPE_STRING),
                'rate': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['author', 'email', 'text', 'rate'],
        ),
        responses={201: ReviewSerializer(many=False)},
        operation_description="add review menu",
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        data = request.data
        review = Review.objects.create(
            author=data['author'],
            email=data['email'],
            text=data['text'],
            date=datetime.now(),
            rate=data['rate'],
            product_id=pk
        )
        serializer = self.serializer_class(review, many=False)
        logger.info(_('Saving a product review by a user %s'), data['author'])
        return Response([serializer.data], status=status.HTTP_201_CREATED)


class ManufacturerListAPIView(APIView):
    """
    Представление для получения производителей.
    """

    @swagger_auto_schema(
        responses={200: ManufacturerSerializer(many=True)},
        operation_description="get product detail",
    )
    def get(self, request: Request) -> Response:
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        logger.info(_('Obtaining manufacturers of goods'))
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerListAPIView(APIView):
    """
    Предсталение для получения продавцов.
    """

    def get(self, request: Request) -> Response:
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        logger.info(_('Getting sellers of goods'))
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecificationAPIView(APIView):
    """
    Представление для получения спецификаций.
    """

    def get(self, request: Request, pk: int) -> Response:
        specifications = Specification.objects.filter(category_id=pk).first()
        serializer = SpecificationSerializer(specifications)
        logger.info(_('Obtaining characteristics for a product category'))
        return Response(serializer.data, status=status.HTTP_200_OK)
