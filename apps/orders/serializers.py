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
    from_city = CitySerializer()
    from_subcity = SubCitySerializer()
    from_label = LabelSerializer()
    to_city = CitySerializer()
    to_subcity = SubCitySerializer()
    product_category = ProductCategorySerializer()

    # Добавляем поле order_id как read_only
    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'from_city', 'from_subcity', 'from_address', 'from_label', 'from_delivery_type',
            'to_city', 'to_subcity', 'to_address', 'to_delivery_type',
            'product_category', 'delivery_cost', 'comment', 'created_at'
        ]

    # Переопределяем метод create
    def create(self, validated_data):
        # Извлекаем вложенные данные
        from_city_data = validated_data.pop('from_city')
        from_subcity_data = validated_data.pop('from_subcity')
        from_label_data = validated_data.pop('from_label', None)
        to_city_data = validated_data.pop('to_city')
        to_subcity_data = validated_data.pop('to_subcity')
        product_category_data = validated_data.pop('product_category')

        # Создаем или получаем вложенные объекты
        from_city, created = City.objects.get_or_create(**from_city_data)
        from_subcity, created = SubCity.objects.get_or_create(city=from_city, **from_subcity_data)
        to_city, created = City.objects.get_or_create(**to_city_data)
        to_subcity, created = SubCity.objects.get_or_create(city=to_city, **to_subcity_data)
        product_category, created = ProductCategory.objects.get_or_create(**product_category_data)

        # Если передан лейбл, обрабатываем его
        from_label = None
        if from_label_data:
            from_label, created = Label.objects.get_or_create(**from_label_data)

        # Создаем основной объект Order с генерацией order_id
        order = Order.objects.create(
            from_city=from_city,
            from_subcity=from_subcity,
            from_label=from_label,
            to_city=to_city,
            to_subcity=to_subcity,
            product_category=product_category,
            **validated_data
        )
        return order

    # Переопределяем метод update
    def update(self, instance, validated_data):
        from_city_data = validated_data.pop('from_city', None)
        from_subcity_data = validated_data.pop('from_subcity', None)
        from_label_data = validated_data.pop('from_label', None)
        to_city_data = validated_data.pop('to_city', None)
        to_subcity_data = validated_data.pop('to_subcity', None)
        product_category_data = validated_data.pop('product_category', None)

        # Обновляем город и подгород откуда
        if from_city_data:
            from_city, created = City.objects.get_or_create(**from_city_data)
            instance.from_city = from_city
        if from_subcity_data:
            from_subcity, created = SubCity.objects.get_or_create(city=instance.from_city, **from_subcity_data)
            instance.from_subcity = from_subcity

        # Обновляем лейбл
        if from_label_data:
            from_label, created = Label.objects.get_or_create(**from_label_data)
            instance.from_label = from_label

        # Обновляем город и подгород куда
        if to_city_data:
            to_city, created = City.objects.get_or_create(**to_city_data)
            instance.to_city = to_city
        if to_subcity_data:
            to_subcity, created = SubCity.objects.get_or_create(city=instance.to_city, **to_subcity_data)
            instance.to_subcity = to_subcity

        # Обновляем категорию товара
        if product_category_data:
            product_category, created = ProductCategory.objects.get_or_create(**product_category_data)
            instance.product_category = product_category

        # Обновляем остальные поля
        instance.from_address = validated_data.get('from_address', instance.from_address)
        instance.to_address = validated_data.get('to_address', instance.to_address)
        instance.from_delivery_type = validated_data.get('from_delivery_type', instance.from_delivery_type)
        instance.to_delivery_type = validated_data.get('to_delivery_type', instance.to_delivery_type)
        instance.delivery_cost = validated_data.get('delivery_cost', instance.delivery_cost)
        instance.comment = validated_data.get('comment', instance.comment)

        instance.save()
        return instance
