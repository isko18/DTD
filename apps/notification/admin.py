from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.notification.models import Notification

User = get_user_model()

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Админка для управления уведомлениями.
    """
    list_display = ['title', 'message', 'url', 'created_at']
    fields = ('title', 'message', 'url',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        """
        При сохранении уведомления, добавляем всех пользователей и создаём записи в Redis.
        """
        # Добавляем всех пользователей к уведомлению
        users = User.objects.all()
        obj.save()
        obj.users.add(*users)
        
        # Создаём Redis записи для отслеживания уведомлений
        obj.create_redis_view()
