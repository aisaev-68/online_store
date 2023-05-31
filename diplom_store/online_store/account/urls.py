from django.urls import include, path
from django.contrib.auth import views
from django.views.generic import TemplateView


from account.views import SettingsAPIView, AccountUser, RegisterView, MyLoginView, MyLogoutView, UserProfileView, UserAvatarView, UserPasswordChangeView, HistoryOrder, ProfileView

app_name = 'account'
urlpatterns = [
    path('api/account/', AccountUser.as_view()),
    path('api/profile/', UserProfileView.as_view()),
    path('api/profile/avatar/', UserAvatarView.as_view()),
    path('api/profile/password/', UserPasswordChangeView.as_view(), name='user-password-change'),
    path('api/history-order/', HistoryOrder.as_view(), name='history_order'),
    path('api/settings/', SettingsAPIView.as_view(), name='settings'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    # path("login/", views.LoginView.as_view(), name="login"),
    # path("logout/", views.LogoutView.as_view(), name="logout"),

]

