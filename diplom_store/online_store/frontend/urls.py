from django.urls import path, include

app_name = 'frontend'
urlpatterns = [
    path("", include('product.urls')),
    path('profile/', include('account.urls')),
    path('orders/', include('order.urls')),
    path('basket/', include('cart.urls')),
    path('payment/', include('payment.urls')),
]
