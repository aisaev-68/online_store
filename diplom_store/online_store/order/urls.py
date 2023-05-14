from django.urls import include, path
from order.views import OrderView, OrderByIdView, OrderActiveView

app_name = 'order'
urlpatterns = [
    path('orders/', OrderView.as_view(), name="order"),
    path('orders/<int:id>/', OrderByIdView.as_view(), name="order_by_id"),
    path('orders/active/', OrderActiveView.as_view(), name="order_active"),
]