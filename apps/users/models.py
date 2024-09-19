from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from PIL import Image

from apps.users.managers import UserManager
from apps.users.utils import generate_verification_code
from apps.utils import custom_upload_path
from core.redis import red


class User(AbstractBaseUser, PermissionsMixin):
    created_at = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    phone_number = models.CharField(
        _("Номер телефона"), max_length=30, unique=True,
    )
    new_phone_number = models.CharField(
        _("Новый номер телефона"), max_length=30, null=True, blank=True
    )
    name = models.CharField(_('ФИО'), max_length=30, blank=True)
    profile_photo = models.ImageField(
        _('Фото профиля'), upload_to=custom_upload_path, null=True, blank=True
    )
    verification_code = models.CharField(
        _('Код подтверждения'), null=True, blank=True, max_length=4
    )
    is_active = models.BooleanField(_('Активный'), default=True)
    fcm_token = models.CharField(
        _('Firebase токен'), max_length=255, blank=True, null=True
    )

    is_staff = models.BooleanField(
        _('Статус staff'), default=False,
        help_text=_(
            'Определяет, может ли пользователь войти на этот сайт '
            'администрирования.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            default_size = 800
            width, height = img.size
            compress_count = width / default_size
            img = img.resize(
                (int(img.size[0] / compress_count),
                 int(img.size[1] / compress_count)),
                Image.Resampling.LANCZOS
            )
            img.save(self.profile_photo.path, quality=80, optimize=True)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        full_name = f'{self.phone_number}: {self.name}'
        return full_name.strip()

    def get_short_name(self):
        return self.name

    def generate_and_save_verification_code(self):
        with transaction.atomic():
            code = generate_verification_code()
            while User.objects.filter(verification_code=code).exists():
                code = generate_verification_code()

            self.verification_code = code
            self.save(update_fields=['verification_code', ])
        return code

    @property
    def notification_view_redis_key(self):
        return f'user:{self.pk};notification:'

    def get_notification_view_status(self):
        keys = red.keys(f'{self.notification_view_redis_key}*')
        return bool(keys)

    def clear_notification_views(self):
        all_keys = red.keys(f'{self.notification_view_redis_key}*')
        if all_keys:
            red.delete(*all_keys)

    @property
    def user_otp_redis_key(self):
        return f'otp;user:{self.pk}'

    @property
    def user_limit_otp_redis_key(self):
        return f'otp_limit;user:{self.pk}'

    def create_otp_limit(self):
        otp_limit_count = red.get(self.user_otp_redis_key)
        if otp_limit_count and int(otp_limit_count) < 2:
            red.incrby(self.user_otp_redis_key, 1)
        elif otp_limit_count and int(otp_limit_count) >= 2:
            red.setex(self.user_limit_otp_redis_key, 20, 1)
        else:
            red.setex(self.user_otp_redis_key, 7200, 1)

    def check_otp_limit(self):
        if red.exists(self.user_limit_otp_redis_key):
            return False
        self.create_otp_limit()
        return True
