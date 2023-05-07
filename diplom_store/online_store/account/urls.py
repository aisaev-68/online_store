from django.urls import include, path
from django.views.generic import TemplateView

from account.api import ProfileView
from account.views import RegisterView, MyLoginView, MyLogoutView, UpdateProfileView, UserAvatarView, HistoryOrder

app_name = 'account'
urlpatterns = [
    path("profile/", UpdateProfileView.as_view(), name='profile'),
    # path('profile/password/', ChangePasswordView.as_view(), name='password_change'),
    path('profile/avatar/', UserAvatarView.as_view(), name='my_account'),
    # path('profile/password/', 'django.contrib.auth.views.password_change', name='password_change'),
    # path('profile/password-change/done/', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('history-order/', HistoryOrder.as_view(), name='history_order'),
]

# urlpatterns = [
#     path('api/profile/', ProfileView.as_view(), name='profile'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', MyLoginView.as_view(), name='login'),
#     path('logout/', MyLogoutView.as_view(), name='logout'),
# ]
