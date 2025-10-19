"""
Утилита для оптимизации изображений
Автоматически сжимает изображения без потери качества
"""

import os
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def optimize_image(image_field, max_width=1920, max_height=1080, quality=85):
    """
    Оптимизирует изображение: уменьшает размер и вес

    Args:
        image_field: Django ImageField или UploadedFile
        max_width: максимальная ширина (по умолчанию 1920px)
        max_height: максимальная высота (по умолчанию 1080px)
        quality: качество JPEG (85 - оптимальный баланс)

    Returns:
        InMemoryUploadedFile: оптимизированное изображение
    """
    if not image_field:
        return None

    # Открываем изображение
    img = Image.open(image_field)

    # Конвертируем RGBA в RGB (для JPEG)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Создаем белый фон
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Получаем оригинальные размеры
    original_width, original_height = img.size

    # Рассчитываем новые размеры с сохранением пропорций
    ratio = min(max_width / original_width, max_height / original_height)

    # Уменьшаем только если изображение больше максимальных размеров
    if ratio < 1:
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Сохраняем в буфер с оптимизацией
    output = BytesIO()

    # Используем прогрессивный JPEG для лучшей загрузки
    img.save(
        output,
        format='JPEG',
        quality=quality,
        optimize=True,
        progressive=True
    )

    output.seek(0)

    # Получаем имя файла без расширения
    original_name = os.path.splitext(image_field.name)[0]
    new_name = f"{original_name}.jpg"

    # Создаем новый InMemoryUploadedFile
    optimized_image = InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )

    return optimized_image


def optimize_icon(image_field, size=200, quality=90):
    """
    Оптимизирует иконку категории (маленькое изображение)

    Args:
        image_field: Django ImageField или UploadedFile
        size: размер иконки (200x200px по умолчанию)
        quality: качество JPEG (90 для иконок)

    Returns:
        InMemoryUploadedFile: оптимизированная иконка
    """
    if not image_field:
        return None

    # Открываем изображение
    img = Image.open(image_field)

    # Конвертируем в RGB
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Создаем квадратную иконку с crop по центру
    width, height = img.size
    min_dimension = min(width, height)

    # Обрезаем по центру
    left = (width - min_dimension) // 2
    top = (height - min_dimension) // 2
    right = left + min_dimension
    bottom = top + min_dimension

    img = img.crop((left, top, right, bottom))

    # Уменьшаем до нужного размера
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Применяем небольшую резкость для четкости иконок
    from PIL import ImageFilter
    img = img.filter(ImageFilter.SHARPEN)

    # Сохраняем в буфер
    output = BytesIO()
    img.save(
        output,
        format='JPEG',
        quality=quality,
        optimize=True
    )

    output.seek(0)

    # Имя файла
    original_name = os.path.splitext(image_field.name)[0]
    new_name = f"{original_name}_icon.jpg"

    # Создаем InMemoryUploadedFile
    optimized_icon = InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )

    return optimized_icon
