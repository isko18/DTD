from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CityViewSet, SubCityViewSet, ProductCategoryViewSet, OrderViewSet

# Создаём роутер
router = DefaultRouter()

# Регистрируем наши ViewSets с роутером
router.register(r'cities', CityViewSet)
router.register(r'subcities', SubCityViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'orders', OrderViewSet)

# Подключаем сгенерированные маршруты
urlpatterns = [
    path('', include(router.urls)),
]
