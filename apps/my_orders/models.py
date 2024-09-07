from django.db import models
from apps.orders.models import Order as BaseOrder  # Импорт основной модели Order
from apps.ransom.models import PurchaseOrder as BasePurchaseOrder  # Импорт основной модели PurchaseOrder

STATUS_CHOICES = [
    ('processing', 'Обработка заказа'),
    ('courier_assigned', 'Назначаем курьера'),
    ('on_the_way', 'Курьер в пути'),
    ('shipped', 'Отгрузка заказа'),
    ('delivered', 'Заказ получен'),
]

class OrderStatus(models.Model):
    # Связываем с моделью Order из приложения orders
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE, verbose_name="Заказ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус заказа")
    estimated_arrival = models.DateField(null=True, blank=True, verbose_name="Примерная дата прибытия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Поле даты создания

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"
        ordering = ['-created_at']  # Упорядочивание по дате создания (последние заказы сверху)
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order {self.order.order_id} - {self.get_status_display()}"

class PurchaseOrderStatus(models.Model):
    # Связываем с моделью PurchaseOrder из приложения ransom
    purchase_order = models.ForeignKey(BasePurchaseOrder, on_delete=models.CASCADE, verbose_name="Выкуп")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус выкупа")
    estimated_arrival = models.DateField(null=True, blank=True, verbose_name="Примерная дата прибытия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Поле даты создания

    class Meta:
        verbose_name = "Статус выкупа"
        verbose_name_plural = "Статусы выкупов"
        ordering = ['-created_at']  # Упорядочивание по дате создания (последние выкупы сверху)
        indexes = [
            models.Index(fields=['purchase_order']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Purchase Order {self.purchase_order.purchase_order_id} - {self.get_status_display()}"
