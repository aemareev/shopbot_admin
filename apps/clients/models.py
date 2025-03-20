from django.db import models


class TelegramUser(models.Model):
    """
    Модель для хранения информации о пользователях Telegram-бота.
    """
    telegram_id = models.BigIntegerField(unique=True, verbose_name="User ID")

    username = models.CharField(max_length=32, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="Фамилия")
    full_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Полное имя")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Клиент Telegram-бота"
        verbose_name_plural = "Клиенты Telegram-бота"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name or self.username or f"User {self.telegram_id}"


