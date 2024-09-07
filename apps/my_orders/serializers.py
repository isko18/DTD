from rest_framework import serializers
from apps.orders.serializers import *
from apps.ransom.serializers import *
from .models import OrderStatus, PurchaseOrderStatus  # Импортируем модели статусов


# Сериализатор для заказа
class OrderSerializer(serializers.ModelSerializer):
    from_city = CitySerializer()
    from_subcity = SubCitySerializer()
    from_label = LabelSerializer()
    to_city = CitySerializer()
    to_subcity = SubCitySerializer()
    product_category = ProductCategorySerializer()

    status = serializers.CharField(source='orderstatus.status', read_only=True)
    estimated_arrival = serializers.DateField(source='orderstatus.estimated_arrival', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_label', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type',
            'product_category', 'delivery_cost', 'comment', 'status', 'estimated_arrival', 'created_at'
        ]


# Сериализатор для выкупа
class PurchaseOrderSerializer(serializers.ModelSerializer):
    from_city = CitySerializer()
    to_city = CitySerializer()
    from_label = LabelSerializer()
    product_category = ProductCategorySerializer()

    status = serializers.CharField(source='purchaseorderstatus.status', read_only=True)
    estimated_arrival = serializers.DateField(source='purchaseorderstatus.estimated_arrival', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'purchase_order_id', 'from_city', 'from_address', 'from_label', 'from_delivery_type',
            'to_city', 'to_address', 'to_delivery_type',
            'sender_name', 'sender_phone',
            'receiver_name', 'receiver_phone',
            'product_category', 'product_name', 'product_url', 'article', 'color', 'price',
            'quantity', 'comment', 'pickup_service', 'keep_shoe_box', 'status', 'estimated_arrival', 'created_at'
        ]
