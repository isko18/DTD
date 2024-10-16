from rest_framework import serializers
from apps.orders.models import City, ProductCategory, SubCity
from .models import PurchaseOrder, PurchaseOrderItem

class SubCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCity
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    subcities = SubCitySerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'subcities']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem  # Исправляем на модель PurchaseOrderItem
        fields = ['id', 'product_category', 'product_name', 'product_url', 'article', 'color', 'price', 'quantity', 'comment']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)  # Добавляем инлайн товары

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type',
            'sender_name', 'sender_phone', 'receiver_name', 'receiver_phone',
            'items', 'pickup_service', 'keep_shoe_box', 'created_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)
        return purchase_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.from_city = validated_data.get('from_city', instance.from_city)
        instance.from_subcity = validated_data.get('from_subcity', instance.from_subcity)
        instance.from_address = validated_data.get('from_address', instance.from_address)
        instance.from_delivery_type = validated_data.get('from_delivery_type', instance.from_delivery_type)
        instance.to_city = validated_data.get('to_city', instance.to_city)
        instance.to_subcity = validated_data.get('to_subcity', instance.to_subcity)
        instance.to_address = validated_data.get('to_address', instance.to_address)
        instance.to_delivery_type = validated_data.get('to_delivery_type', instance.to_delivery_type)
        instance.sender_name = validated_data.get('sender_name', instance.sender_name)
        instance.sender_phone = validated_data.get('sender_phone', instance.sender_phone)
        instance.receiver_name = validated_data.get('receiver_name', instance.receiver_name)
        instance.receiver_phone = validated_data.get('receiver_phone', instance.receiver_phone)
        instance.pickup_service = validated_data.get('pickup_service', instance.pickup_service)
        instance.keep_shoe_box = validated_data.get('keep_shoe_box', instance.keep_shoe_box)
        instance.save()

        instance.items.all().delete()  # Удаляем старые товары
        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=instance, **item_data)

        return instance
