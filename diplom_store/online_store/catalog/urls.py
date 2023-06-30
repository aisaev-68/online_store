from django.urls import include, path
from catalog.views import (
    CategoryAPIView,
    CatalogAPIView,
    ProductPopularAPIView,
    ProductLimitedAPIView,
    SalesAPIView,
    BannersAPIView,
)
from product.views import ManufacturerListAPIView, SellerListAPIView, SpecificationAPIView

app_name = 'catalog'
urlpatterns = [
    path('api/categories/', CategoryAPIView.as_view(), name="category"),
    path('api/catalog/', CatalogAPIView.as_view(), name="catalog"),
    path("api/catalog/<int:pk>/", CatalogAPIView.as_view(), name="catalog_by_id"), #{'get': 'list'}
    path('api/manufacturers/', ManufacturerListAPIView.as_view(), name='manufacturer-list'),
    path('api/sellers/', SellerListAPIView.as_view(), name='seller-list'),
    path('api/specification/<int:pk>/', SpecificationAPIView.as_view()),
    path("api/products/popular/", ProductPopularAPIView.as_view(), name="product_popular"),
    path("api/products/limited/", ProductLimitedAPIView.as_view(), name="product_limited"),
    path("api/sale/", SalesAPIView.as_view(), name="sales"),
    path("api/banners/", BannersAPIView.as_view(), name="banners"),
]