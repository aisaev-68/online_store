from django.urls import include, path
from order.views import OrderView, ConfirmOrderAPIView, OrderActiveAPIView

app_name = 'order'
urlpatterns = [
    path('api/orders/', OrderView.as_view()),
    path('api/orders/<int:pk>/', ConfirmOrderAPIView.as_view()),
    path('api/orders/active/', OrderActiveAPIView.as_view()),
]