import random
import string
from django.db import models
from apps.users.models import User
# Модель города
class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Город")

    def __str__(self):
        return self.name

# Модель подгорода, связанного с городом
class SubCity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подгород")
    city = models.ForeignKey(City, related_name="subcities", on_delete=models.CASCADE, verbose_name="Город")

    def __str__(self):
        return f"{self.name}, {self.city.name}"

# Модель для лейблов
class Label(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название лейбла")

    def __str__(self):
        return self.name

# Модель для категорий товаров
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория товара")

    def __str__(self):
        return self.name

# Модель заказа
class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Обработка заказа'),
        ('document_preparation', 'Оформление груза в Дубае'),
        ('courier_on_way', 'Курьер в пути'),
        ('dispatched', 'Отгрузка заказа'),
        ('received', 'Заказ получен'),
        ('canceled', 'Отменен'),
    ]
    # Пользователь, который сделал заказ
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, verbose_name="Пользователь")

    # Уникальный ID заказа
    order_id = models.CharField(max_length=10, unique=True, blank=True, verbose_name="ID заказа")

    # Добавляем поле статуса
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус заказа")

    # Откуда
    from_city = models.ForeignKey(City, related_name="orders_from_city", on_delete=models.CASCADE, verbose_name="Город откуда")
    from_subcity = models.ForeignKey(SubCity, related_name="orders_from_subcity", on_delete=models.CASCADE, verbose_name="Подгород откуда")
    from_address = models.CharField(max_length=255, verbose_name="Адрес откуда")
    from_label = models.ForeignKey(Label, related_name="orders_from_label", on_delete=models.SET_NULL, null=True, verbose_name="Название лейбла")
    from_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки откуда")

    # Куда
    to_city = models.ForeignKey(City, related_name="orders_to_city", on_delete=models.CASCADE, verbose_name="Город куда")
    to_subcity = models.ForeignKey(SubCity, related_name="orders_to_subcity", on_delete=models.CASCADE, verbose_name="Подгород куда")
    to_address = models.CharField(max_length=255, verbose_name="Адрес куда")
    to_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки куда")

    # О заказе
    product_category = models.ForeignKey(ProductCategory, related_name="orders", on_delete=models.SET_NULL, null=True, verbose_name="Категория товара")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость доставки")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ {self.order_id} от {self.user.username} из {self.from_city.name} в {self.to_city.name}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_unique_order_id()
        super(Order, self).save(*args, **kwargs)

    def generate_unique_order_id(self):
        """
        Генерация уникального ID для заказа
        """
        while True:
            order_id = 'JOG' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id