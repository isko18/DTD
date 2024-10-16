from rest_framework import serializers
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_category = serializers.CharField(source="product_category.name", allow_null=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = ['product_name', 'product_url', 'product_category', 'price', 'article', 'color', 'quantity', 'comment']

class CombinedOrderSerializer(serializers.Serializer):
    order_type = serializers.SerializerMethodField()
    order_id = serializers.CharField()
    estimated_arrival = serializers.CharField(allow_null=True)
    status = serializers.CharField()
    from_city = serializers.CharField(source='from_city.name', allow_null=True)
    from_subcity = serializers.CharField(source='from_subcity.name', allow_null=True)
    from_address = serializers.CharField(allow_null=True)
    from_delivery_type = serializers.CharField(allow_null=True)
    to_city = serializers.CharField(source='to_city.name', allow_null=True)
    to_subcity = serializers.CharField(source='to_subcity.name', allow_null=True)
    to_address = serializers.CharField(allow_null=True)
    to_delivery_type = serializers.CharField(allow_null=True)

    # Поля для товаров
    items = PurchaseOrderItemSerializer(many=True, read_only=True)

    # Поля отправителя и получателя, уникальные для PurchaseOrder
    sender_name = serializers.SerializerMethodField()
    sender_phone = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    receiver_phone = serializers.SerializerMethodField()

    delivery_cost = serializers.SerializerMethodField()
    comment = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    keep_shoe_box = serializers.SerializerMethodField()
    pickup_service = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_order_type(self, obj):
        if isinstance(obj, Order):
            return "regular_order"
        elif isinstance(obj, PurchaseOrder):
            return "purchase_order"
        return "unknown"

    # Методы для получения полей товаров
    def get_items(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.items.all()
        return None

    # Методы для полей отправителя и получателя (только для PurchaseOrder)
    def get_sender_name(self, obj):
        return getattr(obj, 'sender_name', None) if isinstance(obj, PurchaseOrder) else None

    def get_sender_phone(self, obj):
        return getattr(obj, 'sender_phone', None) if isinstance(obj, PurchaseOrder) else None

    def get_receiver_name(self, obj):
        return getattr(obj, 'receiver_name', None) if isinstance(obj, PurchaseOrder) else None

    def get_receiver_phone(self, obj):
        return getattr(obj, 'receiver_phone', None) if isinstance(obj, PurchaseOrder) else None

    def get_delivery_cost(self, obj):
        return getattr(obj, 'delivery_cost', None)

    def get_keep_shoe_box(self, obj):
        return getattr(obj, 'keep_shoe_box', None) if isinstance(obj, PurchaseOrder) else None

    def get_pickup_service(self, obj):
        return getattr(obj, 'pickup_service', None) if isinstance(obj, PurchaseOrder) else None

    # Метод для отображения пользователя
    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'name': obj.user.name,
                'phone_number': obj.user.phone_number
            }
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Убираем None поля из представления
        return {key: value for key, value in representation.items() if value is not None}
