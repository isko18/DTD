from rest_framework import mixins, viewsets
from .models import City, SubCity, Label, ProductCategory, Order
from .serializers import CitySerializer, SubCitySerializer, LabelSerializer, ProductCategorySerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated

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
    # permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут работать с выкупами


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
    # permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут работать с выкупами


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
    # permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут работать с выкупами


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
    # permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут работать с выкупами


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
    # permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут работать с выкупами

