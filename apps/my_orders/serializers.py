from rest_framework import serializers
from apps.orders.models import Order, ProductCategory
from apps.ransom.models import PurchaseOrder, PurchaseOrderItem

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'price_category']  # Добавляем id, name и price_category

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_category = serializers.CharField(source='product_category.name')  # Отображаем только имя категории

    class Meta:
        model = PurchaseOrderItem
        fields = ['product_name', 'product_url', 'product_category', 'price', 'article', 'color', 'quantity', 'keep_shoe_box', 'pickup_service', 'comment']

class CombinedOrderSerializer(serializers.Serializer):
    order_type = serializers.SerializerMethodField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    from_city = serializers.CharField(source='from_city.name', allow_null=True)
    from_subcity = serializers.CharField(source='from_subcity.name', allow_null=True)
    from_address = serializers.CharField(allow_null=True)
    from_delivery_type = serializers.CharField(allow_null=True)
    to_city = serializers.CharField(source='to_city.name', allow_null=True)
    to_subcity = serializers.CharField(source='to_subcity.name', allow_null=True)
    to_address = serializers.CharField(allow_null=True)
    to_delivery_type = serializers.CharField(allow_null=True)
    product_category = serializers.SerializerMethodField()  # Используем метод для гибкости

    # Поля для товаров
    items = PurchaseOrderItemSerializer(many=True, read_only=True)

    # Поля отправителя и получателя для PurchaseOrder
    sender_name = serializers.SerializerMethodField()
    sender_phone = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    receiver_phone = serializers.SerializerMethodField()

    delivery_cost = serializers.CharField(allow_null=True)
    comment = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    user = serializers.SerializerMethodField()

    def get_order_type(self, obj):
        if isinstance(obj, Order):
            return "regular_order"
        elif isinstance(obj, PurchaseOrder):
            return "purchase_order"
        return "unknown"

    def get_product_category(self, obj):
        # Логика для типа PurchaseOrder: только имя категории товара
        if isinstance(obj, PurchaseOrder):
            items = obj.items.all()
            if items.exists():
                return items.first().product_category.name  # Только имя категории
        # Логика для типа Order: категория с именем и ценой
        elif isinstance(obj, Order):
            if obj.product_category:
                return {
                    'id': obj.product_category.id,
                    'name': obj.product_category.name,
                    'price_category': obj.product_category.price_category
                }
        return None

    def get_sender_name(self, obj):
        return getattr(obj, 'sender_name', None) if isinstance(obj, PurchaseOrder) else None

    def get_sender_phone(self, obj):
        return getattr(obj, 'sender_phone', None) if isinstance(obj, PurchaseOrder) else None

    def get_receiver_name(self, obj):
        return getattr(obj, 'receiver_name', None) if isinstance(obj, PurchaseOrder) else None

    def get_receiver_phone(self, obj):
        return getattr(obj, 'receiver_phone', None) if isinstance(obj, PurchaseOrder) else None

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
        return {key: value for key, value in representation.items() if value is not None}
