from firebase_admin import messaging
from firebase_admin.messaging import AndroidConfig, AndroidNotification, APNSConfig, APNSPayload, Aps

def send_push_notification(notification):
    title = notification.title if notification.title else "Новое уведомление"
    body = notification.message if notification.message else "Новость"
    
    try:
        # Получаем FCM токены пользователей, которым нужно отправить уведомление
        fcm_tokens = [
            token for token in notification.users.values_list('fcm_token', flat=True)
            if token is not None
        ]

        # Если нет пользователей с FCM токенами, выходим
        if not fcm_tokens:
            return False

        # Определяем конфигурацию для Android и iOS
        sound = 'default'
        android_config = AndroidConfig(notification=AndroidNotification(sound=sound))
        ios_config = APNSConfig(payload=APNSPayload(aps=Aps(sound=sound)))

        # Отправляем уведомления каждому пользователю
        for fcm_token in fcm_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                android=android_config,  # Конфигурация для Android
                apns=ios_config,  # Конфигурация для iOS
                token=fcm_token
            )
            messaging.send(message)

        return True

    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")
        return False


def send_message_notification(title, body, fcm_token):
    try:
        sound = 'default'
        android_config = AndroidConfig(notification=AndroidNotification(sound=sound))
        ios_config = APNSConfig(payload=APNSPayload(aps=Aps(sound=sound)))

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            android=android_config,  # Конфигурация для Android
            apns=ios_config,  # Конфигурация для iOS
            token=fcm_token,
        )
        messaging.send(message)
        return True
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")
        return False
