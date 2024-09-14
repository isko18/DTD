from rest_framework import viewsets, response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder
from .serializers import CombinedOrderSerializer



class CombinedOrderViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с объединёнными заказами (Order и PurchaseOrder).
    """
    
    def list(self, request):
        """
        Возвращает список всех заказов (обычные и выкупные).
        """
        orders = Order.objects.all()
        purchase_orders = PurchaseOrder.objects.all()
        combined_queryset = list(orders) + list(purchase_orders)
        serializer = CombinedOrderSerializer(combined_queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальные данные о заказе по его order_id.
        """
        try:
            order = Order.objects.get(order_id=pk)
        except Order.DoesNotExist:
            order = get_object_or_404(PurchaseOrder, order_id=pk)
        
        serializer = CombinedOrderSerializer(order)
        return response.Response(serializer.data)
