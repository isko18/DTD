from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import City, SubCity, ProductCategory, Order
from .serializers import CitySerializer, SubCitySerializer, ProductCategorySerializer, OrderSerializer

# Базовый ViewSet для всех CRUD операций
class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass

# Представление для городов (CRUD)
class CityViewSet(BaseViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

# Представление для подгородов (CRUD)
class SubCityViewSet(BaseViewSet):
    queryset = SubCity.objects.all()
    serializer_class = SubCitySerializer

# Представление для категорий товаров (CRUD)
class ProductCategoryViewSet(BaseViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

# Представление для заказов (CRUD)
class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  


    def get_queryset(self):
        # Фильтруем заказы только для текущего аутентифицированного пользователя
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически назначаем заказ аутентифицированному пользователю
        serializer.save(user=self.request.user)
