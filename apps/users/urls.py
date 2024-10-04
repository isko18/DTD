from django.urls import path
from djoser.views import TokenDestroyView
from fcm_django.api.rest_framework import FCMDeviceViewSet

from apps.users import views
from apps.notification.views import NotificationListView, NotificationClearView
from apps.users.views import CustomTokenCreateView, ChangePasswordView

urlpatterns = [
    path('sign-up/', views.UserCreateView.as_view(), name='sign-up'),  # Регистрация
    path('sign-in/', CustomTokenCreateView.as_view(), name="sign-in"),  # Вход через SMS
    path('logout/', TokenDestroyView.as_view(), name="logout"),  # Логаут пользователя
    path('activation/', views.UserActivationView.as_view(), name='activation'),  # Активация пользователя по коду
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password-reset'),  # Сброс пароля через SMS
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),  # Смена пароля
    path('verification-code-sent/', views.UserVerificationCodeSentView.as_view(), name='verification-code-sent'),  # Отправка кода верификации
    path('verification-code-check/', views.UserVerificationCodeCheckView.as_view(), name='verification-code-check'),  # Проверка кода верификации
    path('profile/', views.UserUpdateView.as_view(), name='user-detail'),  # Обновление профиля пользователя
    path('notifications/', NotificationListView.as_view(), name='notification-list'),  # Список уведомлений
    path('notifications/clear/', NotificationClearView.as_view(), name='notification-clear'),  # Очистка уведомлений

    path('change-phone-number/', views.UserChangePhoneNumberView.as_view(), name='change-phone-number'),  # Изменение номера телефона
    path('set-new-phone-number/', views.UserSetNewPhoneNumberView.as_view(), name='set-new-phone-number'),  # Установка нового номера телефона

    # Регистрация и удаление устройства для FCM (Firebase Cloud Messaging)
    path('device/', FCMDeviceViewSet.as_view({'post': 'create'}), name='api-register-device'),  # Регистрация устройства для FCM
    path('device/<registration_id>/', FCMDeviceViewSet.as_view({'delete': 'destroy'}), name='api-destroy-device'),  # Удаление устройства
]
