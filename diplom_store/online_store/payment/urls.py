from django.urls import include, path
from payment.views import PaymentAPIView

app_name = 'payment'
urlpatterns = [
    path('api/payment/<int:pk>/', PaymentAPIView.as_view(), name="payment"),
]