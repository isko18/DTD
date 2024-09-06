from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="17-1B API",
      default_version='v1',
      description="17-1B description",
      terms_of_service="https://t.me/Geeks_Osh_bot",
      contact=openapi.Contact(email="abdykadyrovsyimyk0708@gmail.com"),
      license=openapi.License(name="BSD License"), 
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    path('', include('apps.base.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(api_urlpatterns)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)