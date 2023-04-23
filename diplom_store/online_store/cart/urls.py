
from django.urls import path

from cart.views import BasketView

app_name = 'cart'

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('cart/', BasketView.as_view(), name='cart'),
]