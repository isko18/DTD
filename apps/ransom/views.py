from rest_framework import viewsets, mixins
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

# ViewSet для выкупов заказов
class PurchaseOrderViewSet(
    mixins.ListModelMixin,    # Позволяет получить список выкупов
    mixins.CreateModelMixin,  # Позволяет создать новый выкуп
    mixins.RetrieveModelMixin,  # Позволяет получить конкретный выкуп
    mixins.UpdateModelMixin,  # Позволяет обновить существующий выкуп
    mixins.DestroyModelMixin,  # Позволяет удалить выкуп
    viewsets.GenericViewSet    # Основной класс для ViewSet
):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # Можно добавить дополнительные методы, если необходимо, например, для фильтрации или валидации
