from rest_framework import generics
from rest_framework.response import Response
from .models import OrderStatus, PurchaseOrderStatus
from .serializers import OrderSerializer, PurchaseOrderSerializer

class CombinedOrderListView(generics.ListAPIView):
    """
    Список всех заказов и выкупов.
    """
    def get(self, request, *args, **kwargs):
        # Получение всех заказов и выкупов
        orders = OrderStatus.objects.all()
        purchase_orders = OrderStatus.objects.all()

        # Сериализация данных
        order_serializer = OrderSerializer(orders, many=True)
        purchase_order_serializer = PurchaseOrderSerializer(purchase_orders, many=True)

        # Объединение данных в один список
        combined_list = order_serializer.data + purchase_order_serializer.data

        return Response(combined_list)


class OrderDetailView(generics.RetrieveAPIView):
    """
    Детальный просмотр заказа.
    """
    queryset = OrderStatus.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'  # Используется для поиска заказа по его ID


class PurchaseOrderDetailView(generics.RetrieveAPIView):
    """
    Детальный просмотр выкупа.
    """
    queryset = PurchaseOrderStatus.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'purchase_order_id'  # Используется для поиска выкупа по его ID


# If you want to combine the detail views for both models, consider a single view that handles both:
class CombinedDetailView(generics.GenericAPIView):
    """
    Детальный просмотр заказа или выкупа.
    """
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        purchase_order_id = kwargs.get('purchase_order_id')

        if order_id:
            # Получение и сериализация заказа
            try:
                order = OrderStatus.objects.get(order_id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            except OrderStatus.DoesNotExist:
                return Response({"detail": "Order not found."}, status=404)

        if purchase_order_id:
            # Получение и сериализация выкупа
            try:
                purchase_order = PurchaseOrderStatus.objects.get(purchase_order_id=purchase_order_id)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response(serializer.data)
            except PurchaseOrderStatus.DoesNotExist:
                return Response({"detail": "PurchaseOrder not found."}, status=404)

        return Response({"detail": "Order ID or PurchaseOrder ID must be provided."}, status=400)
