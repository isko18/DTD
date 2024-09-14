from rest_framework import serializers
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder

class CombinedOrderSerializer(serializers.Serializer):
    order_type = serializers.SerializerMethodField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    from_city = serializers.CharField(source='from_city.name')
    from_subcity = serializers.CharField(source='from_subcity.name')
    from_address = serializers.CharField()
    to_city = serializers.CharField(source='to_city.name')
    to_subcity = serializers.CharField(source='to_subcity.name')
    to_address = serializers.CharField()
    product_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    sender_phone = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    receiver_phone = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    delivery_cost = serializers.SerializerMethodField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_order_type(self, obj):
        if isinstance(obj, Order):
            return "regular_order"
        elif isinstance(obj, PurchaseOrder):
            return "purchase_order"

    def get_product_name(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.product_name
        return None  # У обычного заказа нет поля product_name

    def get_price(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.price
        return None

    def get_sender_name(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.sender_name
        return None

    def get_sender_phone(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.sender_phone
        return None

    def get_receiver_name(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.receiver_name
        return None

    def get_receiver_phone(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.receiver_phone
        return None

    def get_article(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.article
        return None

    def get_color(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.color
        return None

    def get_quantity(self, obj):
        if isinstance(obj, PurchaseOrder):
            return obj.quantity
        return None

    def get_delivery_cost(self, obj):
        if isinstance(obj, Order):
            return obj.delivery_cost
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None}
