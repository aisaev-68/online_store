from django.urls import include, path
from order.views import OrderView, OrderByIdView, OrderActiveView

app_name = 'order'
urlpatterns = [
    # path('api/orders/', OrderView.as_view()),
    # path('api/orders/<int:id>/', OrderByIdView.as_view()),
    # path('api/orders/active/', OrderActiveView.as_view()),
]