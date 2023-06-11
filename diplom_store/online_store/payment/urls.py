from django.urls import include, path
from payment.views import PaymentView

app_name = 'payment'
urlpatterns = [
    path('api/payment/', PaymentView.as_view(), name="payment"),
]