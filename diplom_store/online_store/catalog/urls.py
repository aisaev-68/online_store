from django.urls import include, path
from catalog.views import (
    CategoryView,
    CatalogView,
    CatalogByIdView,
    ProductPopularView,
    ProductLimitedView,
    SalesView,
    BannersView,
)
from product.views import ManufacturerListAPIView, SellerListAPIView, SpecificationAPIView

app_name = 'catalog'
urlpatterns = [
    path('api/categories/', CategoryView.as_view(), name="category"),
    path('api/catalog/', CatalogView.as_view(), name="catalog"),
    path("api/catalog/<int:pk>/", CatalogView.as_view(), name="catalog_by_id"), #{'get': 'list'}
    path('api/manufacturers/', ManufacturerListAPIView.as_view(), name='manufacturer-list'),
    path('api/sellers/', SellerListAPIView.as_view(), name='seller-list'),
    path('api/specification/<int:pk>/', SpecificationAPIView.as_view()),
    path("api/products/popular/", ProductPopularView.as_view(), name="product_popular"),
    path("api/products/limited/", ProductLimitedView.as_view(), name="product_limited"),
    path("api/sales/", SalesView.as_view(), name="sales"),
    path("api/banners/", BannersView.as_view(), name="banners"),
]