from rest_framework import serializers
from apps.orders.models import City, ProductCategory, SubCity
from .models import PurchaseOrder

# Сериализатор для подгорода
class SubCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCity
        fields = ['id', 'name']

# Сериализатор для города с подгородами
class CitySerializer(serializers.ModelSerializer):
    subcities = SubCitySerializer(many=True, read_only=True)  # Подгружаем подгорода через related_name

    class Meta:
        model = City
        fields = ['id', 'name', 'subcities']

# Сериализатор для категорий товаров
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

# Основной сериализатор для выкупа заказа
class PurchaseOrderSerializer(serializers.ModelSerializer):
    from_city = CitySerializer()
    from_subcity = SubCitySerializer()
    to_city = CitySerializer()
    to_subcity = SubCitySerializer()
    product_category = ProductCategorySerializer()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type',
            'sender_name', 'sender_phone',
            'receiver_name', 'receiver_phone',
            'product_category', 'product_name', 'product_url', 'article', 'color', 'price',
            'quantity', 'comment', 'pickup_service', 'keep_shoe_box', 'created_at'
        ]

    def create(self, validated_data):
        from_city_data = validated_data.pop('from_city')
        from_subcity_data = validated_data.pop('from_subcity')
        to_city_data = validated_data.pop('to_city')
        to_subcity_data = validated_data.pop('to_subcity')
        product_category_data = validated_data.pop('product_category')

        # Получение или создание вложенных объектов
        from_city, _ = City.objects.get_or_create(**from_city_data)
        from_subcity, _ = SubCity.objects.get_or_create(city=from_city, **from_subcity_data)
        to_city, _ = City.objects.get_or_create(**to_city_data)
        to_subcity, _ = SubCity.objects.get_or_create(city=to_city, **to_subcity_data)
        product_category, _ = ProductCategory.objects.get_or_create(**product_category_data)

        # Создание основного объекта PurchaseOrder
        purchase_order = PurchaseOrder.objects.create(
            from_city=from_city,
            from_subcity=from_subcity,
            to_city=to_city,
            to_subcity=to_subcity,
            product_category=product_category,
            **validated_data
        )
        return purchase_order

    def update(self, instance, validated_data):
        from_city_data = validated_data.pop('from_city', None)
        from_subcity_data = validated_data.pop('from_subcity', None)
        to_city_data = validated_data.pop('to_city', None)
        to_subcity_data = validated_data.pop('to_subcity', None)
        product_category_data = validated_data.pop('product_category', None)

        # Обновляем вложенные данные
        if from_city_data:
            from_city, _ = City.objects.get_or_create(**from_city_data)
            instance.from_city = from_city
        if from_subcity_data:
            from_subcity, _ = SubCity.objects.get_or_create(city=from_city, **from_subcity_data)
            instance.from_subcity = from_subcity

        if to_city_data:
            to_city, _ = City.objects.get_or_create(**to_city_data)
            instance.to_city = to_city
        if to_subcity_data:
            to_subcity, _ = SubCity.objects.get_or_create(city=to_city, **to_subcity_data)
            instance.to_subcity = to_subcity

        if product_category_data:
            product_category, _ = ProductCategory.objects.get_or_create(**product_category_data)
            instance.product_category = product_category

        # Обновляем остальные данные
        instance.from_address = validated_data.get('from_address', instance.from_address)
        instance.to_address = validated_data.get('to_address', instance.to_address)
        instance.from_delivery_type = validated_data.get('from_delivery_type', instance.from_delivery_type)
        instance.to_delivery_type = validated_data.get('to_delivery_type', instance.to_delivery_type)
        instance.sender_name = validated_data.get('sender_name', instance.sender_name)
        instance.sender_phone = validated_data.get('sender_phone', instance.sender_phone)
        instance.receiver_name = validated_data.get('receiver_name', instance.receiver_name)
        instance.receiver_phone = validated_data.get('receiver_phone', instance.receiver_phone)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_url = validated_data.get('product_url', instance.product_url)
        instance.article = validated_data.get('article', instance.article)
        instance.color = validated_data.get('color', instance.color)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.pickup_service = validated_data.get('pickup_service', instance.pickup_service)
        instance.keep_shoe_box = validated_data.get('keep_shoe_box', instance.keep_shoe_box)

        instance.save()
        return instance
