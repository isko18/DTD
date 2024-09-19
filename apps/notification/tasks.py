from celery import shared_task

from notification.models import Notification


@shared_task
def send_notification_from_admin(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.send()
    return "Notification sent"
