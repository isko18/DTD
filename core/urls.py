from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройки для документации Swagger и ReDoc
schema_view = get_schema_view(
   openapi.Info(
      title="DTA API",
      default_version='v1',
      description="API для проекта DTA",
      terms_of_service="#",
      contact=openapi.Contact(email="support@dta.com"),
      license=openapi.License(name="DTA License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Пути для включения различных приложений
apps_includes = [
    path('orders/', include('apps.orders.urls')), 
    path('ransom/', include('apps.ransom.urls')), 
    path('my_orders/', include('apps.my_orders.urls')),  
    path('users/', include('apps.users.urls')),  
    # path('carts/', include('apps.carts.urls')),  
    # path('billing/', include('apps.billing.urls')),  
]

# API-роуты
api_urlpatterns = [
    path('api/v1/', include(apps_includes)),
]

# Основные пути проекта
urlpatterns = [
    path('admin/', admin.site.urls),  # Админка

    # Подключение API
    path('', include(api_urlpatterns)),

    # Swagger и ReDoc для документации
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Статические и медиафайлы
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
