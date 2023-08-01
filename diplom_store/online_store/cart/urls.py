
from django.urls import path

from cart.views import BasketAPIView, CartAPIView

app_name = 'cart'

urlpatterns = [
    path('api/cart/', CartAPIView.as_view(), name='cart'),
    path('api/basket/', BasketAPIView.as_view(), name='basket'),
]