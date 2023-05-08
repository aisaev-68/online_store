from django.urls import include, path
from product.views import (
    ProductPopularView,
    SalesView,
    BannerView,
    ProductDetailView,
    ProductReviewView, ProductLimitedView, MainPageView,
)

app_name = 'product'
urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('products/popular/<int:category>/', ProductPopularView.as_view(), name="product-popular"),
    path("products/limited/", ProductLimitedView.as_view()),
    path('sales/', SalesView.as_view()),
    path('banners/', BannerView.as_view()),
    path('product/<int:id>/', ProductDetailView.as_view({'get': 'retrieve'})),
    path('product/<int:id>/review/', ProductReviewView.as_view()),
]
