from django.db import models

from apps.cart.models import Cart
from apps.clients.models import TelegramClient


class Order(models.Model):
    """Модель заказа."""

    STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменен"),
    ]

    client = models.ForeignKey(TelegramClient, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders",
                             verbose_name="Корзина")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус")
    shipping_address = models.TextField(verbose_name="Адрес доставки")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ {self.pk} для {self.client}"

    def calculate_total_price(self):
        """Вычисляем общую стоимость заказа на основе товаров в корзине."""
        total = sum(item.get_total_price() for item in self.cart.items.all())
        return total

    def save(self, *args, **kwargs):
        """Перед сохранением рассчитываем общую стоимость и очищаем корзину клиента."""
        self.total_price = self.calculate_total_price()

        # Очищаем корзину после создания заказа
        if self.cart:
            self.cart.items.all().delete()  # Удаляем все товары из корзины

        super().save(*args, **kwargs)
