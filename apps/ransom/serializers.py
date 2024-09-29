from rest_framework import serializers
from apps.orders.models import City, ProductCategory, SubCity
from .models import PurchaseOrder

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

class PurchaseOrderSerializer(serializers.ModelSerializer):
    from_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    from_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    to_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    to_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = [
            'id','user', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type',
            'sender_name', 'sender_phone',
            'receiver_name', 'receiver_phone',
            'product_category', 'product_name', 'product_url', 'article', 'color', 'price',
            'quantity', 'comment', 'pickup_service', 'keep_shoe_box', 'created_at'
        ]

    def create(self, validated_data):
        return PurchaseOrder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
