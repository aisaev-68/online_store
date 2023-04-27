from django.urls import include, path
from account.views import RegisterView, MyLoginView, MyLogoutView, ChangePasswordView, UserProfileView, UserAvatarView

app_name = 'account'
urlpatterns = [
    path("profile/", UserProfileView.as_view(), name='profile'),
    path('profile/password/', ChangePasswordView.as_view()),
    path('profile/avatar/', UserAvatarView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
