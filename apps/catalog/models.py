import os
from io import BytesIO
from uuid import uuid4

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models


def product_image_upload_path(instance, filename):
    """
    Формирует путь для загрузки изображений товаров.
    Например: products/550e8400-e29b-41d4-a716-446655440000.jpeg
    """
    filename = f"{uuid4()}.jpeg"  # Всегда используем расширение .jpeg
    return os.path.join("products", filename)


class Category(models.Model):
    """
    Модель категории товаров.
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Модель подкатегории товаров.
    """
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Product(models.Model):
    """
    Модель товара.
    """
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="products", verbose_name="Подкатегория"
    )
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True,
                              verbose_name="Изображение товара")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Переопределяем метод save для обработки изображения.
        """
        if self.image:
            # Открываем изображение с помощью Pillow
            img = Image.open(self.image)

            # Изменяем размер изображения до 800x800 пикселей
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)

            # Конвертируем изображение в JPEG
            if img.format != 'JPEG':
                img = img.convert('RGB')  # Конвертируем в RGB для JPEG

            # Сохраняем изображение в BytesIO
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)  # Сохраняем в формате JPEG
            buffer.seek(0)

            # Сохраняем обработанное изображение в поле image
            self.image.save(
                os.path.basename(self.image.name),  # Имя файла
                ContentFile(buffer.read()),  # Содержимое файла
                save=False  # Не сохраняем модель, чтобы избежать рекурсии
            )

        # Вызываем оригинальный метод save
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path  # Получаем полный путь к файлу
            if os.path.isfile(image_path):  # Проверяем, существует ли файл
                try:
                    os.remove(image_path)  # Удаляем файл
                    print(f"Image {image_path} deleted successfully.")
                except Exception as e:
                    print(f"Error deleting image {image_path}: {e}")
            else:
                print(f"Image {image_path} not found.")

        super().delete(*args, **kwargs)
