from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.custom_serializers import CustomDateTimeField
from apps.notification.models import Notification


class NotificationPushSerializer(ModelSerializer):
    """
    Сериализатор для отправки минимальных данных уведомления, например, через push-уведомления.
    """
    class Meta:
        model = Notification
        fields = ('message',)


class NotificationSerializer(ModelSerializer):
    """
    Основной сериализатор для отображения уведомлений.
    """
    created_at = CustomDateTimeField()  # Форматирование времени создания
    is_new_notification = serializers.SerializerMethodField()  # Поле для проверки новых уведомлений

    def get_is_new_notification(self, instance):
        """
        Метод для проверки, является ли уведомление новым для пользователя.
        """
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        return instance.get_user_viewed_status(user=user)  # Проверяем статус через метод модели

    class Meta:
        model = Notification
        fields = (
            'pk', 'created_at', 'title', 'message',  # Основные поля уведомления
            'is_new_notification', 'url'  # Дополнительные поля
        )
