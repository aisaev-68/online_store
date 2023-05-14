from django.urls import include, path
from catalog.views import (
    CategoryView,
    CatalogView,
    BannersView,
    TagsView,
)

app_name = 'catalog'
urlpatterns = [
    path('api/categories/', CategoryView.as_view(), name="category"),
    path('api/catalog/', CatalogView.as_view(), name="catalog"),
    path("banners/", BannersView.as_view(), name="banners"),
    path("tags/", TagsView.as_view(), name="tags"),

]