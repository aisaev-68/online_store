from django.urls import path, re_path
from django.views.generic import TemplateView
from account.views import RegisterView, MyLoginView, MyLogoutView


name = 'frontend'
urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html"), name='index'),
    path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('delivery/', TemplateView.as_view(template_name="frontend/delivery.html"), name='delivery'),
    path('account/', TemplateView.as_view(template_name="frontend/account.html"), name='account'),
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html"), name='cart'),
    re_path(r'^catalog/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('catalog/<int:pk>', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('order-detail/<int:pk>', TemplateView.as_view(template_name="frontend/oneorder.html"), name="oneorder"),
    path('order/', TemplateView.as_view(template_name="frontend/order.html")),
    path('payment/', TemplateView.as_view(template_name="frontend/payment.html"), name='payment'),
    path('payment/<int:pk>/', TemplateView.as_view(template_name="frontend/payment.html"), name='payment-detail'),
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html"), name="payment-someone"),
    path('product/<int:pk>/', TemplateView.as_view(template_name="frontend/product.html"), name='product'),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html")),
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html"), name="progress-payment"),
    path('sale/', TemplateView.as_view(template_name="frontend/sale.html")),
    path('settings/', TemplateView.as_view(template_name="frontend/settings.html")),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
