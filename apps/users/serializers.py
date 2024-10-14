from django.contrib.auth import get_user_model, authenticate
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from core.redis import red
from djoser.serializers import (
    UserCreatePasswordRetypeSerializer, PasswordRetypeSerializer,
    TokenSerializer, TokenCreateSerializer
)
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.users.constants import (
    OTP_ERROR_MESSAGE, USER_NOT_EXISTS_ERROR,
    OTP_LIMIT_ERROR_MESSAGE
)
from apps.users.mixins import PhoneNumberValidateMixin
from apps.users.otp import send_nikita_sms
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserCreateSerializer(PhoneNumberValidateMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "phone_number", "name", 'fcm_token')  # Пароль удален

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)
                if not user.check_otp_limit():
                    raise ValidationError(OTP_LIMIT_ERROR_MESSAGE)

                is_code_sent = send_nikita_sms(user)  # Отправляем SMS с кодом
                if not is_code_sent:
                    raise ValidationError(OTP_ERROR_MESSAGE)
                print("User successfully registered and SMS sent.")
        except IntegrityError as e:
            raise PermissionDenied(detail="User is already registered")
        return user


class BaseVerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True, max_length=4)

    class Meta:
        fields = ('verification_code', 'phone_number')

    def validate(self, attrs):
        verification_code = self.initial_data.get("verification_code")
        phone_number = self.initial_data.get("phone_number")
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError(
                {"phone_number": USER_NOT_EXISTS_ERROR})
        if user.verification_code != verification_code:
            raise serializers.ValidationError(
                {"verification_code": _("Неверный код подтверждения")}
            )
        self.instance = user
        return attrs


class UserActivationSerializer(PhoneNumberValidateMixin, BaseVerificationCodeSerializer):
    phone_number = serializers.CharField(required=True, max_length=30)

    class Meta:
        fields = ('verification_code', 'phone_number')

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.verification_code = None
        instance.save(update_fields=['verification_code', 'is_active'])
        return instance

    def to_representation(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        data = UserDetailSerializer(instance).data
        data.update({
            "auth_token": token.key
        })
        return data

class CustomTokenCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=30)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise ValidationError(USER_NOT_EXISTS_ERROR)

        # Проверяем лимит на отправку OTP через Redis
        redis_key = f'sms_sent:user:{user.pk}'
        if red.exists(redis_key):
            raise ValidationError(_("SMS уже отправлено, повторите попытку позже."))

        # Отправляем SMS с кодом
        is_code_sent = send_nikita_sms(user)
        if not is_code_sent:
            raise ValidationError(OTP_ERROR_MESSAGE)

        # Сохраняем в Redis метку о том, что SMS было отправлено
        red.setex(redis_key, 300, 1)  # Время истечения — 5 минут

        attrs['user'] = user  # Передаем пользователя дальше
        return attrs



class UserSignInSerializer(TokenSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            UserDetailSerializer(instance.user).data
        )
        return data


class UserVerificationCodeSentSerializer(PhoneNumberValidateMixin, serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=30)

    class Meta:
        fields = ('phone_number',)

    def validate(self, attrs):
        phone_number = self.initial_data.get("phone_number")
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise ValidationError({"phone_number": USER_NOT_EXISTS_ERROR})
        self.instance = user
        return attrs

    def update(self, instance, validated_data):
        if not instance.check_otp_limit():
            raise ValidationError(OTP_LIMIT_ERROR_MESSAGE)
        is_code_sent = send_nikita_sms(instance)
        if not is_code_sent:
            raise ValidationError(OTP_ERROR_MESSAGE)
        return instance

    def to_representation(self, instance):
        return {"message": _("Код верификации успешно отправлен")}


class UserVerificationCodeCheckSerializer(PhoneNumberValidateMixin, BaseVerificationCodeSerializer):
    phone_number = serializers.CharField(required=True, max_length=30)
    verification_code = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ('verification_code', 'phone_number')

    def update(self, instance, validated_data):
        instance.verification_code = None
        instance.save(update_fields=['verification_code', ])  # Очищаем код
        return instance

    def to_representation(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        return {"auth_token": token.key, "message": _("Номер успешно подтвержден")}

class UserPasswordResetSerializer(PhoneNumberValidateMixin, PasswordRetypeSerializer):
    phone_number = serializers.CharField(required=True, max_length=30)

    def validate(self, attrs):
        phone_number = self.initial_data.get("phone_number")
        self.user = User.objects.filter(phone_number=phone_number).first()
        if not self.user:
            raise serializers.ValidationError(
                {"phone_number": USER_NOT_EXISTS_ERROR})
        attrs = super().validate(attrs)
        self.instance = self.user
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance

    def to_representation(self, instance):
        return {"message": _("Пароль успешно обновлен")}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("Новый пароль не должен совпадать со старым паролем.")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(read_only=False, required=False)
    has_new_notifications = serializers.BooleanField(
        source='get_notification_view_status'
    )

    class Meta:
        model = User
        fields = (
            'pk', 'name', 'profile_photo', 'phone_number',
            'fcm_token', 'has_new_notifications'
        )
        read_only_fields = (
            'phone_number', 'has_new_notifications'
        )


class UserChangePhoneNumberSerializer(PhoneNumberValidateMixin, serializers.ModelSerializer):

    def validate_new_phone_number(self, value):
        new_phone_number = super().validate_phone_number(value)
        if User.objects.filter(
                Q(phone_number=new_phone_number) |
                Q(new_phone_number=new_phone_number)).exists():
            raise ValidationError(_("Номер телефона уже занят"))
        return value

    class Meta:
        model = User
        fields = ("new_phone_number",)

    def update(self, instance, validated_data):
        with transaction.atomic():
            super().update(instance, validated_data)
            if not instance.check_otp_limit():
                raise ValidationError(OTP_LIMIT_ERROR_MESSAGE)
            new_phone_number = validated_data['new_phone_number']
            is_code_sent = send_nikita_sms(instance, new_phone_number)
            if not is_code_sent:
                raise ValidationError(OTP_ERROR_MESSAGE)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {"message": _("На номер телефона отправлен код верификации")}
        )
        return data


class UserSetNewPhoneNumberSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True, max_length=4)

    class Meta:
        fields = ('verification_code',)

    def validate_verification_code(self, value):
        if self.instance.verification_code != value:
            raise serializers.ValidationError(_("Неверный код подтверждения"))
        return value

    def validate(self, attrs):
        if not self.instance.new_phone_number:
            raise ValidationError(
                {"new_phone_number": _("Вы еще не указали новый номер")}
            )
        if self.instance.phone_number == self.instance.new_phone_number:
            raise ValidationError(
                {"new_phone_number": _("Данный номер телефона уже занят")}
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.phone_number = instance.new_phone_number
                instance.new_phone_number = None
                instance.verification_code = None
                instance.save()
            except IntegrityError:
                raise ValidationError(
                    {"new_phone_number": _("Данный номер телефона уже занят")}
                )
        return instance

    def to_representation(self, instance):
        return {"message": _("Ваш номер телефона был изменен")}