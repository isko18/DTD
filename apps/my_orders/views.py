from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder
from .serializers import CombinedOrderSerializer


class CombinedOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Только для аутентифицированных пользователей

    def list(self, request):
        user = request.user

        # Фильтруем заказы и выкупы только для текущего пользователя
        orders = Order.objects.filter(user=user)
        purchase_orders = PurchaseOrder.objects.filter(user=user)

        # Логирование для отладки
        print(f"Orders: {orders}")
        print(f"Purchase Orders: {purchase_orders}")

        # Объединяем запросы
        combined_queryset = list(orders) + list(purchase_orders)

        # Логирование после объединения
        print(f"Combined Queryset: {combined_queryset}")

        # Сериализуем данные
        serializer = CombinedOrderSerializer(combined_queryset, many=True)
        
        # Логирование сериализованных данных
        print(f"Serialized Data: {serializer.data}")

        return response.Response(serializer.data)

