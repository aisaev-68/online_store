from django.urls import include, path
from order.views import OrderHistoryAPiView, OrderAPIView, OrderActiveAPIView

app_name = 'order'
urlpatterns = [
    path('api/orders/', OrderHistoryAPiView.as_view()),
    path('api/orders/<int:pk>/', OrderAPIView.as_view()),
    path('api/orders/active/', OrderActiveAPIView.as_view()),
]