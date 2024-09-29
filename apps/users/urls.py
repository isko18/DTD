from django.urls import path

from djoser.views import TokenCreateView, TokenDestroyView
from fcm_django.api.rest_framework import FCMDeviceViewSet

from apps.users import views
from apps.notification.views import NotificationListView, NotificationClearView
from apps.users.views import CustomTokenCreateView, ChangePasswordView

urlpatterns = [
    path('sign-up/', views.UserCreateView.as_view(), name='sign-up'),
    path('sign-in/', CustomTokenCreateView.as_view(), name="sign-in"),
    path('logout/', TokenDestroyView.as_view(), name="logout"),
    path('activation/', views.UserActivationView.as_view(), name='activation'),
    path('password_reset', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('verification_code_sent/', views.UserVerificationCodeSentView.as_view(), name='verification_code_sent'),
    path('verification_code_check/', views.UserVerificationCodeCheckView.as_view(), name='verification_code_check'),
    path('profile/', views.UserUpdateView.as_view(), name='user_detail'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/clear/', NotificationClearView.as_view(), name='notification_clear'),

    path('change_phone_number/', views.UserChangePhoneNumberView.as_view(), name='change_phone_number'),
    path('set_new_phone_number/', views.UserSetNewPhoneNumberView.as_view(), name='set_new_phone_number'),

    path('device/', FCMDeviceViewSet.as_view({'post': 'create'}), name='api_register_device'),
    path('device/<registration_id>/', FCMDeviceViewSet.as_view({'delete': 'destroy'})),

]
