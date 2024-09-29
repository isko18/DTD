from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from rest_framework.authtoken.models import Token


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'phone_number', 'name', 'is_active', 'is_staff', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('phone_number', 'name')
    ordering = ('created_at',)

    # Поля, которые нельзя редактировать
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('name', 'profile_photo', 'fcm_token')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    # Для создания токена прямо из админки
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Token.objects.get_or_create(user=obj)

# Регистрация кастомной модели пользователя
admin.site.register(User, UserAdmin)
