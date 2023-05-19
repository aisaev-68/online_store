from django.urls import include, path
from django.views.generic import TemplateView


from account.views import RegisterView, MyLoginView, MyLogoutView, UserProfileView, UserAvatarView, UserPasswordChangeView, HistoryOrder, ProfileView

app_name = 'account'
urlpatterns = [
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/avatar/', UserAvatarView.as_view(), name='user-avatar'),
    path('api/profile/password/', UserPasswordChangeView.as_view(), name='user-password-change'),
    path("profile/", ProfileView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('history-order/', HistoryOrder.as_view(), name='history_order'),
]

