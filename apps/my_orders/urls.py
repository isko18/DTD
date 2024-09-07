from django.urls import path
from .views import CombinedOrderListView, OrderDetailView, PurchaseOrderDetailView

urlpatterns = [
    # Список заказов и выкупов
    path('my_orders/', CombinedOrderListView.as_view(), name='order-list'),
    
    # Детальный просмотр заказа
    path('orders/<str:order_id>/', OrderDetailView.as_view(), name='order-detail'),

    # Детальный просмотр выкупа
    path('purchase-orders/<str:purchase_order_id>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
]