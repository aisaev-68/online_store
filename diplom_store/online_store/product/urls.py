from django.urls import path
from product.views import (
    ProductDetailView,
    ProductReviewView, MainPageView
)

app_name = 'product'
urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('api/product/<int:id>/', ProductDetailView.as_view({'get': 'retrieve'})),
    path('api/product/<int:id>/review/', ProductReviewView.as_view()),

]
