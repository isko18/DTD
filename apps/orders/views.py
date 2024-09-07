from rest_framework import mixins, viewsets
from .models import City, SubCity, Label, ProductCategory, Order
from .serializers import CitySerializer, SubCitySerializer, LabelSerializer, ProductCategorySerializer, OrderSerializer

# Представление для городов (CRUD)
class CityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet  # Изменение здесь
):
    queryset = City.objects.all()
    serializer_class = CitySerializer

# Представление для подгородов (CRUD)
class SubCityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet  # Изменение здесь
):
    queryset = SubCity.objects.all()
    serializer_class = SubCitySerializer

# Представление для лейблов (CRUD)
class LabelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet  # Изменение здесь
):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

# Представление для категорий товаров (CRUD)
class ProductCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet  # Изменение здесь
):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

# Представление для заказов (CRUD)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet  # Изменение здесь
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
