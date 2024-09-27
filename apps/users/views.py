from django.contrib.auth import get_user_model
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from apps.users.serializers import (
    UserCreateSerializer, UserVerificationCodeCheckSerializer,
    UserVerificationCodeSentSerializer, UserActivationSerializer,
    UserPasswordResetSerializer, UserDetailSerializer,
    UserChangePhoneNumberSerializer, UserSetNewPhoneNumberSerializer, CustomTokenCreateSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = CustomTokenCreateSerializer

    def _action(self, serializer):
        # Получаем пользователя по номеру телефона
        user = User.objects.filter(phone_number=serializer.data.get('phone_number')).first()

        # Проверка, что пользователь существует
        if not user:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка активности пользователя
        if not user.is_active:
            return Response({"detail": "Пользователь не активен."}, status=status.HTTP_403_FORBIDDEN)

        # Создание токена для пользователя
        token = utils.login_user(self.request, user)
        token_serializer_class = settings.SERIALIZERS.token

        # Получаем данные токена
        data = token_serializer_class(token).data

        # Обновляем FCM токен, если он передан
        if serializer.data.get('fcm_token'):
            user.fcm_token = serializer.data.get('fcm_token')
            user.save()

        # Возвращаем данные токена
        return Response(data=data, status=status.HTTP_200_OK)

class BaseUserPostView(GenericAPIView):
    serializer_class = None

    def perform_post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = self.perform_post(request)
        return Response(data, status=status.HTTP_200_OK)


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Only for flutter mobile"""
        user_is_exists = User.objects.filter(phone_number=request.data.get(
            'phone_number')).exists()
        if user_is_exists:
            raise PermissionDenied(detail="User already exists")
        return super().create(request, *args, **kwargs)


class UserActivationView(BaseUserPostView):
    http_method_names = ('post',)
    serializer_class = UserActivationSerializer
    permission_classes = (AllowAny,)


class UserVerificationCodeSentView(BaseUserPostView):
    http_method_names = ('post',)
    serializer_class = UserVerificationCodeSentSerializer
    permission_classes = (AllowAny,)


class UserVerificationCodeCheckView(BaseUserPostView):
    http_method_names = ('post',)
    serializer_class = UserVerificationCodeCheckSerializer
    permission_classes = (AllowAny,)


class UserPasswordResetView(BaseUserPostView):
    http_method_names = ('post',)
    serializer_class = UserPasswordResetSerializer
    permission_classes = (AllowAny,)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Проверяем старый пароль
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Старый пароль неверен."]}, status=status.HTTP_400_BAD_REQUEST)

            # Устанавливаем новый пароль
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@parser_classes((MultiPartParser,))
class UserUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user


class UserChangePhoneNumberView(BaseUserPostView):
    serializer_class = UserChangePhoneNumberSerializer

    def perform_post(self, request):
        serializer = self.serializer_class(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class UserSetNewPhoneNumberView(BaseUserPostView):
    serializer_class = UserSetNewPhoneNumberSerializer

    def perform_post(self, request):
        serializer = self.serializer_class(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
