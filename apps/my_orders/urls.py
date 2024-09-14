from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CombinedOrderViewSet

# Создаем роутер
router = DefaultRouter()
router.register(r'my_orders', CombinedOrderViewSet, basename='combined-order')

# Подключаем роутер к URL
urlpatterns = [
    path('', include(router.urls)),
]