from django.contrib import admin

from apps.clients.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Отображение пользователей Telegram в админке."""

    list_display = ("telegram_id", "username", "full_name", "created_at")
    search_fields = ("telegram_id", "username", "full_name")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
