from django.db import models

from apps.catalog.models import Product
from apps.clients.models import TelegramClient


class Cart(models.Model):
    """
    Корзина товаров, привязанная к клиенту.
    """
    client = models.OneToOneField(TelegramClient, on_delete=models.CASCADE, related_name="cart", verbose_name="Клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.client}"


class CartItem(models.Model):
    """
    Позиция в корзине (конкретный товар с количеством).
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def get_total_price(self):
        """Возвращает стоимость данного товара с учетом количества."""
        return self.product.price * self.quantity
