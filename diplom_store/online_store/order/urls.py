from django.urls import include, path
from order.views import OrderHistoryAPiView, OrderAPIView, OrderActiveAPIView

app_name = 'order'
urlpatterns = [
    path('api/orders/', OrderHistoryAPiView.as_view(), name='history-order'),
    path('api/orders/<int:pk>/', OrderAPIView.as_view(), name='order'),
    path('api/orders/active/', OrderActiveAPIView.as_view(), name='active-order'),
]