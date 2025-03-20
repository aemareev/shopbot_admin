import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import Product


def delete_old_image(image_path):
    """Удаляет файл изображения, если он существует"""
    if image_path and os.path.isfile(image_path):
        try:
            os.remove(image_path)
            print(f"✅ Файл {image_path} успешно удален.")
        except Exception as e:
            print(f"⚠️ Ошибка при удалении файла {image_path}: {e}")


@receiver(pre_save, sender=Product)
def delete_old_image_before_update(sender, instance, **kwargs):
    """
    Удаляет старое изображение перед загрузкой нового.
    """
    if not instance.pk:  # Если объект новый, не выполняем код
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Если изображение изменилось, удаляем старый файл
    if old_instance.image and old_instance.image != instance.image:
        delete_old_image(old_instance.image.path)


@receiver(post_delete, sender=Product)
def delete_image_after_delete(sender, instance, **kwargs):
    """
    Удаляет изображение после удаления объекта из базы данных.
    """
    if instance.image:
        delete_old_image(instance.image.path)
