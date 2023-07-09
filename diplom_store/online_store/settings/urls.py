from django.urls import path

from settings.views import SettingsAPIView



app_name = 'settings'
urlpatterns = [
    path('api/settings/', SettingsAPIView.as_view(), name='settings'),
]