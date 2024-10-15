from rest_framework import serializers
from apps.orders.models import Order
from apps.ransom.models import PurchaseOrder

class CombinedOrderSerializer(serializers.Serializer):
    order_type = serializers.SerializerMethodField()
    order_id = serializers.CharField()
    estimated_arrival = serializers.CharField()
    status = serializers.CharField()
    from_city = serializers.CharField(source='from_city.name')
    from_subcity = serializers.CharField(source='from_subcity.name')
    from_address = serializers.CharField()
    from_delivery_type = serializers.CharField()
    to_delivery_type = serializers.CharField()
    to_city = serializers.CharField(source='to_city.name')
    to_subcity = serializers.CharField(source='to_subcity.name')
    to_address = serializers.CharField()
    product_name = serializers.SerializerMethodField()
    product_url = serializers.SerializerMethodField()
    product_category = serializers.CharField()
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
    keep_shoe_box = serializers.SerializerMethodField()
    pickup_service = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_order_type(self, obj):
        if isinstance(obj, Order):
            return "regular_order"
        elif isinstance(obj, PurchaseOrder):
            return "purchase_order"
        return "unknown"

    def get_product_name(self, obj):
        return getattr(obj, 'product_name', None)

    def get_product_url(self, obj):
        return getattr(obj, 'product_url', None)

    def get_price(self, obj):
        return getattr(obj, 'price', None)

    def get_sender_name(self, obj):
        return getattr(obj, 'sender_name', None)

    def get_sender_phone(self, obj):
        return getattr(obj, 'sender_phone', None)

    def get_receiver_name(self, obj):
        return getattr(obj, 'receiver_name', None)

    def get_receiver_phone(self, obj):
        return getattr(obj, 'receiver_phone', None)

    def get_article(self, obj):
        return getattr(obj, 'article', None)

    def get_color(self, obj):
        return getattr(obj, 'color', None)

    def get_quantity(self, obj):
        return getattr(obj, 'quantity', None)

    def get_estimated_arrival(self, obj):
        return getattr(obj, 'estimated_arrival', None)

    def get_keep_shoe_box(self, obj):
        return getattr(obj, 'keep_shoe_box', None)

    def get_pickup_service(self, obj):
        return getattr(obj, 'pickup_service', None)

    def get_delivery_cost(self, obj):
        return getattr(obj, 'delivery_cost', None)

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
