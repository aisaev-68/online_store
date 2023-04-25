from django.urls import include, path
from account.views import UserView, UserChangePasswordView, UserAvatarView, \
    RegisterView, MyLoginView, MyLogoutView, ChangePasswordView, UserProfileView

app_name = 'account'
urlpatterns = [
    path("profile/", UserProfileView.as_view()),
    path('profile/password/', ChangePasswordView.as_view()),
    path('profile/avatar/', UserAvatarView.as_view({'post': 'update'})),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
