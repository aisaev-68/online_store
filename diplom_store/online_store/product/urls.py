from django.urls import path
from product.views import (
    ProductDetailView,
    ProductReviewView, MainPageView
)

app_name = 'product'
urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('api/product/<int:pk>/', ProductDetailView.as_view()),
    path('api/product/<int:pk>/review/', ProductReviewView.as_view()),

]
