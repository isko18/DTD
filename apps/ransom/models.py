import string
import random
from django.db import models
from apps.orders.models import City, SubCity, ProductCategory

def generate_unique_order_id():
    """Генерация уникального идентификатора для заказа."""
    return 'JOG' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('order_processing', 'Обработка заказа'),
        ('assigning_courier', 'Назначаем курьера'),
        ('courier_on_way', 'Курьер в пути'),
        ('order_shipped', 'Отгрузка заказа'),
        ('order_received', 'Заказ получен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='order_processing', verbose_name="Статус")
    estimated_arrival = models.DateTimeField(null=True, blank=True, verbose_name="Примерное время прибытия")
    order_id = models.CharField(max_length=10, unique=True, editable=False, verbose_name="ID заказа")
    from_city = models.ForeignKey(City, related_name="purchase_orders_from_city", on_delete=models.CASCADE, verbose_name="Город откуда")
    from_subcity = models.ForeignKey(SubCity, related_name="purchase_orders_from_subcity", on_delete=models.CASCADE, verbose_name="Подгород откуда")
    from_address = models.CharField(max_length=255, verbose_name="Адрес откуда")
    from_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки откуда")
    to_city = models.ForeignKey(City, related_name="purchase_orders_to_city", on_delete=models.CASCADE, verbose_name="Город куда")
    to_subcity = models.ForeignKey(SubCity, related_name="purchase_orders_to_subcity", on_delete=models.CASCADE, verbose_name="Подгород куда")
    to_address = models.CharField(max_length=255, verbose_name="Адрес куда")
    to_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки куда")
    sender_name = models.CharField(max_length=100, verbose_name="Имя отправителя")
    sender_phone = models.CharField(max_length=20, verbose_name="Телефон отправителя")
    receiver_name = models.CharField(max_length=100, verbose_name="Имя получателя")
    receiver_phone = models.CharField(max_length=20, verbose_name="Телефон получателя")
    product_category = models.ForeignKey(ProductCategory, related_name="purchase_orders", on_delete=models.SET_NULL, null=True, verbose_name="Категория товара")
    product_name = models.CharField(max_length=255, verbose_name="Название товара")
    product_url = models.URLField(verbose_name="Ссылка на товар")
    article = models.CharField(max_length=100, verbose_name="Артикул")
    color = models.CharField(max_length=50, verbose_name="Цвет товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    pickup_service = models.BooleanField(default=False, verbose_name="Услуга вылова товара")
    keep_shoe_box = models.BooleanField(default=False, verbose_name="Сохранить коробку из под обуви")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Выкуп {self.product_name} для {self.receiver_name} ({self.from_city} -> {self.to_city})"

    class Meta:
        verbose_name = "Выкуп заказа"
        verbose_name_plural = "Выкупы заказов"
        ordering = ['-created_at']  # Сортировка по дате создания (последние записи будут первыми)

    def save(self, *args, **kwargs):
        # Генерация уникального идентификатора, если его нет
        if not self.order_id:
            self.order_id = generate_unique_order_id()
        super(PurchaseOrder, self).save(*args, **kwargs)
