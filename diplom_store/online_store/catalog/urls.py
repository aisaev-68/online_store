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

app_name = 'catalog'
urlpatterns = [
    path('api/categories/', CategoryView.as_view(), name="category"),
    path('api/catalog/', CatalogView.as_view(), name="catalog"),
    path("api/catalog/<int:id>/", CatalogByIdView.as_view(), name="catalog_by_id"),
    path("api/products/popular/", ProductPopularView.as_view(), name="product_popular"),
    path("api/products/limited/", ProductLimitedView.as_view(), name="product_limited"),
    path("api/sales/", SalesView.as_view(), name="sales"),
    path("api/banners/", BannersView.as_view(), name="banners"),
]