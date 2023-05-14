from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Swagger Diploma Project",
      default_version='1.0.0',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls, name="admin"),
    path('', include('catalog.urls')),
    path('', include('product.urls')),
    path('', include('account.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),
    path('i18n', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = _('Панель администрирования магазина MEGANO')
admin.site.site_header = _('Админ панель MEGANO Shop')
admin.site.site_title = _('MEGANO Shop')