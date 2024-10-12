from rest_framework.decorators import action
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder
from .serializers import CombinedOrderSerializer

class CombinedOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # Фильтруем заказы и выкупы для текущего пользователя, исключая завершенные
        orders = Order.objects.filter(user=user).exclude(status='order_completed')
        purchase_orders = PurchaseOrder.objects.filter(user=user).exclude(status='order_completed')

        # Объединяем запросы
        combined_queryset = list(orders) + list(purchase_orders)

        # Сериализуем данные
        serializer = CombinedOrderSerializer(combined_queryset, many=True)
        return response.Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed_orders(self, request):
        user = request.user

        # Фильтруем завершенные заказы
        completed_orders = Order.objects.filter(user=user, status='order_completed')
        completed_purchase_orders = PurchaseOrder.objects.filter(user=user, status='order_completed')

        # Объединяем завершенные заказы
        completed_queryset = list(completed_orders) + list(completed_purchase_orders)

        # Сериализуем завершенные заказы
        serializer = CombinedOrderSerializer(completed_queryset, many=True)
        return response.Response(serializer.data)
