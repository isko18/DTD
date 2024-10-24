import random
import string
from django.db import models
from django.conf import settings 
from apps.notification.send_notification import send_push_notification 
from apps.notification.models import Notification  # Импортируем модель Notification


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Город")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class SubCity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подгород")
    city = models.ForeignKey(City, related_name="subcities", on_delete=models.CASCADE, verbose_name="Город")

    def __str__(self):
        return f"{self.name}, {self.city.name}"
    
    class Meta:
        verbose_name = "Подгород"
        verbose_name_plural = "Подгорода"

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория товара")
    price_category = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товара"

class Order(models.Model):
    STATUS_CHOICES = [
        ('order_processing', 'Обработка заказа'),
        ('assigning_courier', 'Назначаем курьера'),
        ('courier_on_way', 'Курьер в пути'),
        ('order_shipped', 'Отгрузка заказа'),
        ('order_received', 'Заказ получен'),
        ('order_completed', 'Завершен'),
        
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='order_processing', verbose_name="Статус")
    estimated_arrival = models.DateTimeField(null=True, blank=True, verbose_name="Примерное время прибытия")
    order_id = models.CharField(max_length=10, unique=True, editable=False, verbose_name="ID заказа")
    from_city = models.ForeignKey(City, related_name="orders_from_city", on_delete=models.CASCADE, verbose_name="Город откуда")
    from_subcity = models.ForeignKey(SubCity, related_name="orders_from_subcity", on_delete=models.CASCADE, verbose_name="Подгород откуда")
    from_address = models.CharField(max_length=255, verbose_name="Адрес откуда")
    from_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки откуда")
    to_city = models.ForeignKey(City, related_name="orders_to_city", on_delete=models.CASCADE, verbose_name="Город куда")
    to_subcity = models.ForeignKey(SubCity, related_name="orders_to_subcity", on_delete=models.CASCADE, verbose_name="Подгород куда")
    to_address = models.CharField(max_length=255, verbose_name="Адрес куда")
    to_delivery_type = models.CharField(max_length=50, choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], verbose_name="Тип доставки куда")
    receiver_name = models.CharField(max_length=100, verbose_name="Имя получателя")
    receiver_phone = models.CharField(max_length=20, verbose_name="Телефон получателя")
    product_category = models.ForeignKey(ProductCategory, related_name="orders", on_delete=models.SET_NULL, null=True, verbose_name="Категория товара")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость доставки", blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders_users", verbose_name="Пользователь")

    def __str__(self):
        return f"Заказ {self.order_id} из {self.from_city.name} в {self.to_city.name}"

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Проверяем, новый ли это заказ
        if not self.order_id:
            self.order_id = self.generate_unique_order_id()

        # Получаем предыдущий статус заказа
        previous_status = None
        if self.pk:
            previous_status = Order.objects.get(pk=self.pk).status

        super(Order, self).save(*args, **kwargs)

        # Логика для отправки уведомления при создании заказа
        if is_new:
            self.send_creation_notification()

        # Логика для отправки уведомления при изменении статуса
        if not is_new and previous_status != self.status:
            self.send_status_change_notification()

    def generate_unique_order_id(self):
        while True:
            order_id = 'JOG' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id

    def send_creation_notification(self):
        """
        Отправка уведомления при создании заказа.
        """
        message = f"Ваш заказ {self.order_id} был успешно создан."
        notification = Notification(
            title="Создание заказа",
            message=message,
        )
        notification.save()  # Сначала сохраняем уведомление

        notification.users.set([self.user])  # Теперь присваиваем пользователей
        notification.save()  # Сохраняем снова для обновления M2M поля

        send_push_notification(notification)  # Передаём объект уведомления

    def send_status_change_notification(self):
        """
        Отправка уведомления при изменении статуса заказа.
        """
        message = f"Статус вашего заказа {self.order_id} изменен на {self.get_status_display()}."
        notification = Notification(
            title="Изменение статуса заказа",
            message=message,
        )
        notification.save()  # Сначала сохраняем уведомление

        notification.users.set([self.user])  # Теперь присваиваем пользователей
        notification.save()  # Сохраняем снова для обновления M2M поля

        send_push_notification(notification)  # Передаём объект уведомления

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']