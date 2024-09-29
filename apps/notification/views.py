from django.utils.translation import gettext_lazy as _

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.notification.models import Notification
from apps.notification.serailizers import NotificationSerializer


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(users=user)

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        user = self.request.user
        user.clear_notification_views()
        return response


class NotificationClearView(APIView):
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        for notification in user.notifications.all():
            notification.users.remove(user)
            if not notification.users.exists():
                notification.delete()
        user.clear_notification_views()
        return Response(
            {'message': _('Все уведомления очищены')},
            status=status.HTTP_200_OK
        )
