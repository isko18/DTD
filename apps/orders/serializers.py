from rest_framework import serializers
from .models import City, SubCity, ProductCategory, Order

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

class OrderSerializer(serializers.ModelSerializer):
    from_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    from_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    to_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    to_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type', 'product_category',
            'delivery_cost', 'comment', 'created_at'
        ]
