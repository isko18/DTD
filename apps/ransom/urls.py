from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet

# Создаем роутер и регистрируем ViewSet для выкупов заказов
router = DefaultRouter()
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchaseorder')

# Основные URL
urlpatterns = [
    path('', include(router.urls)),  # Включаем все маршруты, зарегистрированные в роутере
]
