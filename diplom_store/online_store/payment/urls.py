from django.urls import include, path
from payment.views import PaymentAPIView

app_name = 'payment'
urlpatterns = [
    path('api/payment/', PaymentAPIView.as_view(), name="payment"),
]