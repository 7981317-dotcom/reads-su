"""
Django management команда для оптимизации существующих изображений
Использование: python manage.py optimize_existing_images
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
from articles.models import Article, Category, ArticleMedia


class Command(BaseCommand):
    help = 'Оптимизирует все существующие изображения на сервере'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать, что будет оптимизировано, без фактической оптимизации',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('Режим DRY RUN - изображения не будут изменены'))

        total_saved = 0
        total_images = 0

        # Оптимизация обложек статей
        self.stdout.write('\n📰 Оптимизация обложек статей...')
        articles = Article.objects.exclude(cover_image='')
        for article in articles:
            if article.cover_image:
                saved = self.optimize_image(
                    article.cover_image.path,
                    max_width=1920,
                    max_height=1080,
                    quality=85,
                    dry_run=dry_run
                )
                if saved:
                    total_saved += saved
                    total_images += 1
                    self.stdout.write(f'  ✓ {article.title[:50]}... ({saved} байт)')

        # Оптимизация иконок категорий
        self.stdout.write('\n📁 Оптимизация иконок категорий...')
        categories = Category.objects.exclude(icon_image='')
        for category in categories:
            if category.icon_image:
                saved = self.optimize_image(
                    category.icon_image.path,
                    max_width=200,
                    max_height=200,
                    quality=90,
                    dry_run=dry_run
                )
                if saved:
                    total_saved += saved
                    total_images += 1
                    self.stdout.write(f'  ✓ {category.name} ({saved} байт)')

        # Оптимизация медиа-файлов
        self.stdout.write('\n🖼️  Оптимизация медиа-файлов в статьях...')
        media_images = ArticleMedia.objects.filter(media_type='image')
        for media in media_images:
            if media.file:
                saved = self.optimize_image(
                    media.file.path,
                    max_width=1920,
                    max_height=1080,
                    quality=85,
                    dry_run=dry_run
                )
                if saved:
                    total_saved += saved
                    total_images += 1
                    self.stdout.write(f'  ✓ {media.article.title[:50]}... ({saved} байт)')

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS(f'\n✅ Готово!'))
        self.stdout.write(f'Оптимизировано изображений: {total_images}')
        self.stdout.write(f'Сэкономлено места: {self.format_bytes(total_saved)}')

    def optimize_image(self, image_path, max_width, max_height, quality, dry_run=False):
        """
        Оптимизирует одно изображение

        Returns:
            int: количество сэкономленных байт
        """
        if not os.path.exists(image_path):
            return 0

        try:
            # Получаем размер оригинала
            original_size = os.path.getsize(image_path)

            if dry_run:
                return original_size // 2  # Примерная экономия

            # Открываем изображение
            img = Image.open(image_path)

            # Конвертируем в RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Получаем размеры
            original_width, original_height = img.size

            # Рассчитываем новые размеры
            ratio = min(max_width / original_width, max_height / original_height)

            # Уменьшаем только если нужно
            if ratio < 1:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Создаем временный файл
            temp_path = f"{image_path}.temp.jpg"

            # Сохраняем оптимизированное изображение
            img.save(
                temp_path,
                format='JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )

            # Получаем новый размер
            new_size = os.path.getsize(temp_path)

            # Если новый файл меньше - заменяем оригинал
            if new_size < original_size:
                # Удаляем оригинал
                os.remove(image_path)

                # Переименовываем новый файл
                new_path = os.path.splitext(image_path)[0] + '.jpg'
                os.rename(temp_path, new_path)

                saved = original_size - new_size
                return saved
            else:
                # Если новый файл больше - удаляем его
                os.remove(temp_path)
                return 0

        except Exception as e:
            self.stderr.write(f'  ✗ Ошибка при оптимизации {image_path}: {e}')
            return 0

    def format_bytes(self, bytes):
        """Форматирует байты в человекочитаемый формат"""
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} ТБ"
