from rest_framework import serializers
from .models import City, SubCity, Label, ProductCategory, Order

# Сериализатор для подгорода
class SubCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCity
        fields = ['id', 'name']

# Сериализатор для города
class CitySerializer(serializers.ModelSerializer):
    subcities = SubCitySerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'subcities']

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

# Сериализатор для заказа
class OrderSerializer(serializers.ModelSerializer):
    from_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    from_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    from_label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), allow_null=True, required=False)
    to_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    to_subcity = serializers.PrimaryKeyRelatedField(queryset=SubCity.objects.all())
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())

    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_label', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type', 'product_category', 'delivery_cost', 'comment', 'created_at'
        ]

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
