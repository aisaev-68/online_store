from django.urls import path
from tag.views import TagsView

app_name = 'tag'
urlpatterns = [
    path("api/tags/", TagsView.as_view(), name="tags"),
]