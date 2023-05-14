from django.urls import include, path
from product.views import (
    ProductPopularView,
    SalesView,
    BannerView,
    ProductDetailView,
    ProductReviewView, ProductLimitedView, MainPageView, ProductCatalogView, FilterAndSort
)

app_name = 'product'
urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    # path('products/catalogs/<int:category>/', ProductCatalogView.as_view(), name="product-catalog"),
    path('products/catalogs/<int:category>/', FilterAndSort.as_view(), name="product-catalog"),
    path('products/popular/', ProductPopularView.as_view(), name="product-popular"),
    path("products/limited/", ProductLimitedView.as_view()),
    path('sales/', SalesView.as_view()),
    path('banners/', BannerView.as_view()),
    path('product/<int:id>/', ProductDetailView.as_view({'get': 'retrieve'})),
    path('product/<int:id>/review/', ProductReviewView.as_view()),
]
