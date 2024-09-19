from django.contrib.auth import get_user_model

from apps.notification.send_notification import send_message_notification
from fcm_django.models import FCMDevice

User = get_user_model()


def check_and_send_push_notification(title, user_id, body):
    user = User.objects.get(pk=user_id)
    devices = FCMDevice.objects.filter(user=user_id, active=True)
    if not devices and not user.fcm_token:
        return "Не отправлено. Нет fcm_token"
    if devices:
        for device in devices:
            send_message_notification(
                title=title,
                body=body,
                fcm_token=device.registration_id
            )
            return "Отправлено"
    else:
        send_message_notification(
            title="У вас новое предложение. Проверьте свои заявки",
            body=body,
            fcm_token=user.fcm_token
        )
        return "Отправлено"