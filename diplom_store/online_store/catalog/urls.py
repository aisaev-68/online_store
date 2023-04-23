from django.urls import include, path
from catalog.views import (
    CategoryView,
    CatalogView,
    BannersView,
    TagsView,
)

app_name = 'catalog'
urlpatterns = [
    path('categories/', CategoryView.as_view(), name="category"),
    path("banners/", BannersView.as_view(), name="banners"),
    path("tags/", TagsView.as_view(), name="tags"),
    path('catalog/', CatalogView.as_view(), name="catalog"),
]