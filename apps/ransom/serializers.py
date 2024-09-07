from rest_framework import serializers
from apps.orders.models import City, Label, ProductCategory
from .models import PurchaseOrder

# Сериализатор для города
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

# Сериализатор для лейблов
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']

# Сериализатор для категорий товаров
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

# Основной сериализатор для выкупа заказа
class PurchaseOrderSerializer(serializers.ModelSerializer):
    from_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    to_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    from_label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), allow_null=True)
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), allow_null=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_id', 'from_city', 'from_address', 'from_label', 'from_delivery_type',
            'to_city', 'to_address', 'to_delivery_type',
            'sender_name', 'sender_phone',
            'receiver_name', 'receiver_phone',
            'product_category', 'product_name', 'product_url', 'article', 'color', 'price',
            'quantity', 'comment', 'pickup_service', 'keep_shoe_box', 'created_at'
        ]
        read_only_fields = ['order_id', 'created_at']  # Эти поля не могут быть изменены напрямую

    def create(self, validated_data):
        # Создание нового заказа
        return PurchaseOrder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Обновляем все поля автоматически
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
