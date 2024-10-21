from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from core.redis import red
from apps.utils import custom_upload_path
from ckeditor.fields import RichTextField

# Create your models here.

class Banner(models.Model):
    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

    title = models.CharField(_("Название"), max_length=100)
    sub_title = models.CharField(
        _("Подзаголовок"), max_length=100, null=True
    )
    description = models.TextField(_("Описание"))
    image = models.ImageField(_('Изображение'), upload_to=custom_upload_path)
    url = models.URLField(_('Ссылка'))
    is_active = models.BooleanField(_('Активный'), default=True)
    count = models.PositiveIntegerField(default=0, verbose_name='Количество посещений', editable=False)

    def __str__(self):
        return self.title

    def increment_click_count(self, user_id):
        """
        Увеличивает счетчик кликов, если пользователь не заходил на страницу в течение последней минуты.
        :param user_id: Идентификатор пользователя
        """
        banner_id = self.id
        redis_key = f'banner:{banner_id}:user:{user_id}'
        # Проверяем, был ли пользователь уже на этой странице в течение последней минуты
        if not red.exists(redis_key):
            self.count += 1
            self.save()
            # Устанавливаем ключ в Redis с истечением срока действия в 60 секунд
            red.setex(redis_key, timedelta(minutes=1), 1)


class AboutApp(SingletonModel):
    description = models.TextField(_("Описание"))
    privacy_policy = models.URLField(
        _("Политика конфиденциальности"), blank=True, null=True
    )
    data_processing_policy = models.URLField(
        _("Политика обработки данных"), blank=True, null=True
    )

    def __str__(self):
        return 'О приложении'

    class Meta:
        verbose_name = _('О приложении')
        verbose_name_plural = _('О приложении')


class VersionControl(SingletonModel):
    android_version = models.CharField(
        max_length=255, verbose_name="Версия приложения"
    )
    android_force_update = models.BooleanField(
        default=False, verbose_name="Принудительное обновление"
    )
    ios_version = models.CharField(
        max_length=255, verbose_name="Версия приложения"
    )
    ios_force_update = models.BooleanField(
        default=False, verbose_name="Принудительное обновление"
    )

    class Meta:
        verbose_name = "Управление версией приложения"

    def __str__(self):
        return f'Android: {self.android_version}    IOS: {self.ios_version}'


class FAQ(models.Model):
    question = models.TextField(_('Вопрос'))
    answer = models.TextField(_('Ответ'))
    my_order = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name=_('Очередь')
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('Вопросы и ответы')
        verbose_name_plural = _('Вопросы и ответы')
        ordering = ['my_order']


class Ad(SingletonModel):
    title = models.CharField(_('Заголовок'), max_length=100)
    sub_title = models.CharField(
        _('Подзаголовок'), max_length=100, blank=True, null=True
    )
    description = models.TextField(_('Описание'))
    image = models.ImageField(_('Изображение'), upload_to=custom_upload_path)
    my_order = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name=_('Очередь')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Реклама')
        verbose_name_plural = _('Рекламы')
        ordering = ['my_order']


class Support(SingletonModel):
    phone_number = models.CharField(
        _("Номер телефона для поддержки"), max_length=20
    )
    ad_phone_number = models.CharField(
        _("Номер телефона для рекламы"), max_length=20
    )

    def __str__(self):
        return 'Поддержка'

    class Meta:
        verbose_name = _('Поддержка')
        verbose_name_plural = _('Поддержка')



class PrivacyPolicy(models.Model):
    descriptions = RichTextField(
        verbose_name='ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ'
    ) 
    
    def __str__(self) -> str:
        return self.descriptions
    
    class Meta:
        verbose_name = _("ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ")
        verbose_name_plural = _("ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ")
        
        
class OfferAgreement(models.Model):
    descriptions = RichTextField(
        verbose_name='ДОГОВОР ОФЕРТЫ'
    ) 
    
    def __str__(self) -> str:
        return self.descriptions
    
    class Meta:
        verbose_name = _("ДОГОВОР ОФЕРТЫ")
        verbose_name_plural = _("ДОГОВОР ОФЕРТЫ")