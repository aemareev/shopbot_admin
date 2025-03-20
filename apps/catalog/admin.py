from django.contrib import admin
from django.utils.html import format_html

from .models import Category, SubCategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для модели Category.
    """
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Админка для модели SubCategory.
    """
    list_display = ('name', 'category',)
    list_filter = ('category',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка для модели Product.
    """
    list_display = (
        'name', 'price', 'subcategory', 'get_category', 'image_preview'
    )  # Поля, которые будут отображаться в списке
    list_filter = ('subcategory__category', 'subcategory')  # Фильтры по полям
    search_fields = ('name', 'description', 'subcategory__name')  # Поля, по которым можно искать
    list_per_page = 20  # Количество элементов на странице
    readonly_fields = ('image_preview',)  # Поле для предпросмотра изображения

    @admin.display(description='Категория')
    def get_category(self, obj):
        """
        Возвращает категорию товара через подкатегорию.
        """
        return obj.subcategory.category.name

    @admin.display(description='Превью изображения')
    def image_preview(self, obj):
        """
        Возвращает HTML-код для предпросмотра изображения.
        """
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "Нет изображения"
