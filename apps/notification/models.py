import redis

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.redis import red

User = get_user_model()

class Notification(models.Model):
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    users = models.ManyToManyField(User, related_name='notifications')
    title = models.CharField(
        verbose_name=_("Название"), max_length=150, null=True, blank=True
    )
    message = models.TextField(verbose_name=_("Сообщение"))
    url = models.URLField(verbose_name=_("Ссылка"), null=True, blank=True)

    NEWS_TOPIC = "news"

    def __str__(self):
        if self.title:
            return self.title
        return str(self.pk)

    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering = ["created_at"]

    # Создание записи в Redis для каждого пользователя, который получит уведомление
    def create_redis_view(self):
        for user in self.users.all():
            redis_key = f"{user.notification_view_redis_key}{self.pk}"
            red.set(redis_key, 1)

    # Проверка, видел ли пользователь уведомление, через Redis
    def get_user_viewed_status(self, user):
        redis_key = f"{user.notification_view_redis_key}{self.pk}"
        return bool(red.exists(redis_key))

    # Метод для отправки уведомлений (оставлено на случай будущего использования)
    def send(self):
        from notification.send_notification import send_push_notification

        topic = None
        if self.for_topic:
            topic = self.NEWS_TOPIC
        send_push_notification(notification=self, topic=topic)
