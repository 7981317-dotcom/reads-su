#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для генерации favicon в разных размерах
"""

import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_favicon_png(size, output_path):
    """
    Создает PNG favicon указанного размера
    """
    # Создаем изображение
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Рисуем фон (темно-синий, скругленный)
    padding = size // 16
    radius = size // 5

    # Background rectangle с скруглением
    draw.rounded_rectangle(
        [(padding, padding), (size - padding, size - padding)],
        radius=radius,
        fill='#0F172A'
    )

    # Рисуем букву R
    font_size = int(size * 0.6)
    try:
        # Пытаемся загрузить системный шрифт
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            # Если не получилось, используем дефолтный
            font = ImageFont.load_default()

    # Центрируем текст
    text = "R"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]

    # Рисуем букву (голубой цвет)
    draw.text((x, y), text, fill='#60A5FA', font=font)

    # Сохраняем
    img.save(output_path, 'PNG')
    print(f"[OK] Created: {output_path} ({size}x{size})")


def create_ico_from_pngs(png_paths, output_path):
    """
    Создает .ico файл из нескольких PNG
    """
    images = []
    for png_path in png_paths:
        if os.path.exists(png_path):
            img = Image.open(png_path)
            images.append(img)

    if images:
        images[0].save(
            output_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images]
        )
        print(f"[OK] Created: {output_path}")


# Создаем папку для favicon, если её нет
output_dir = 'static/images/favicons'
os.makedirs(output_dir, exist_ok=True)

print("Generating favicons...")
print("=" * 60)

# Генерируем разные размеры
sizes = [16, 32, 48, 64, 128, 180, 192, 512]
png_paths = []

for size in sizes:
    output_path = f'{output_dir}/favicon-{size}x{size}.png'
    create_favicon_png(size, output_path)
    png_paths.append(output_path)

# Создаем favicon.ico (16x16, 32x32, 48x48)
ico_paths = [f'{output_dir}/favicon-{s}x{s}.png' for s in [16, 32, 48]]
create_ico_from_pngs(ico_paths, 'static/images/favicon.ico')

# Создаем apple-touch-icon.png (180x180)
apple_touch_icon = f'{output_dir}/favicon-180x180.png'
if os.path.exists(apple_touch_icon):
    import shutil
    shutil.copy(apple_touch_icon, 'static/images/apple-touch-icon.png')
    print(f"[OK] Created: static/images/apple-touch-icon.png")

# Создаем android-chrome (192x192, 512x512)
for size in [192, 512]:
    src = f'{output_dir}/favicon-{size}x{size}.png'
    dst = f'static/images/android-chrome-{size}x{size}.png'
    if os.path.exists(src):
        import shutil
        shutil.copy(src, dst)
        print(f"[OK] Created: {dst}")

print("=" * 60)
print("[SUCCESS] All favicons generated!")
print("\nFiles created:")
print("- static/images/favicon.ico")
print("- static/images/apple-touch-icon.png")
print("- static/images/android-chrome-192x192.png")
print("- static/images/android-chrome-512x512.png")
print("- static/images/favicons/ (all sizes)")
