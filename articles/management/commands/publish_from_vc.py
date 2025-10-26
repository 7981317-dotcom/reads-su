"""
Django management команда для публикации статей с VC.ru на reads.su

Использование:
    python manage.py publish_from_vc "Статьи/название-папки-статьи" --category=marketing
"""

import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.base import ContentFile
from articles.models import Article, Category
from PIL import Image
import io

User = get_user_model()


class Command(BaseCommand):
    help = 'Публикует статью с VC.ru на сайт'

    def add_arguments(self, parser):
        parser.add_argument(
            'article_folder',
            type=str,
            help='Путь к папке со статьей (например: Статьи/название-статьи)'
        )
        parser.add_argument(
            '--category',
            type=str,
            default='marketing',
            help='Slug категории для публикации (по умолчанию: marketing)'
        )
        parser.add_argument(
            '--author',
            type=str,
            default='admin',
            help='Username автора (по умолчанию: admin)'
        )

    def handle(self, *args, **options):
        article_folder = options['article_folder']
        category_slug = options['category']
        author_username = options['author']

        self.stdout.write(self.style.SUCCESS(f'\n[*] Начинаем публикацию статьи из: {article_folder}'))

        # Проверка существования папки
        if not os.path.exists(article_folder):
            self.stdout.write(self.style.ERROR(f'[!] Папка не найдена: {article_folder}'))
            return

        # Загрузка метаданных
        metadata_path = os.path.join(article_folder, 'metadata.json')
        if not os.path.exists(metadata_path):
            self.stdout.write(self.style.ERROR(f'[!] Файл metadata.json не найден'))
            return

        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Загрузка контента
        article_path = os.path.join(article_folder, 'article.md')
        if not os.path.exists(article_path):
            self.stdout.write(self.style.ERROR(f'[!] Файл article.md не найден'))
            return

        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Получение автора
        try:
            author = User.objects.get(username=author_username)
            self.stdout.write(f'[+] Автор: {author.username}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'[!] Пользователь {author_username} не найден'))
            return

        # Получение категории
        try:
            category = Category.objects.get(slug=category_slug)
            self.stdout.write(f'[+] Категория: {category.name}')
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'[!] Категория {category_slug} не найдена'))
            self.stdout.write('Доступные категории:')
            for cat in Category.objects.all():
                self.stdout.write(f'  - {cat.slug}: {cat.name}')
            return

        # Создание слага из заголовка
        title = metadata['title']
        slug = self._create_slug(title)

        # Проверка существования статьи с таким слагом
        if Article.objects.filter(slug=slug).exists():
            self.stdout.write(self.style.WARNING(f'[!] Статья с slug "{slug}" уже существует'))
            slug = f"{slug}-{Article.objects.count() + 1}"
            self.stdout.write(f'[+] Использую новый slug: {slug}')

        # Создание статьи (без подзаголовка, чтобы не дублировался)
        article = Article(
            title=title,
            slug=slug,
            subtitle='',  # Оставляем пустым
            content=content,
            excerpt=self._create_excerpt(content),
            author=author,
            category=category,
            status='published',
            featured=False
        )

        # Обработка обложки (первое изображение)
        images_info = metadata.get('images', [])
        if images_info:
            first_image_info = images_info[0]
            image_path = os.path.join(article_folder, 'images', first_image_info['filename'])

            if os.path.exists(image_path):
                self.stdout.write(f'[...] Загружаем обложку: {first_image_info["filename"]}')

                # Оптимизация изображения
                optimized_image = self._optimize_image(image_path)

                # Сохранение обложки
                article.cover_image.save(
                    first_image_info['filename'],
                    ContentFile(optimized_image),
                    save=False
                )
                self.stdout.write(self.style.SUCCESS('[+] Обложка загружена'))

        # Сохранение статьи
        article.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] Статья опубликована!'))
        self.stdout.write(f'[+] ID: {article.id}')
        self.stdout.write(f'[+] Slug: {article.slug}')
        self.stdout.write(f'[+] URL: https://reads.su/article/{article.slug}/')

        # Загрузка всех изображений и обновление путей в контенте
        if images_info:
            self.stdout.write('[...] Загружаем изображения в контент...')
            updated_content = self._upload_and_update_images(content, article, article_folder, images_info)
            article.content = updated_content
            article.save(update_fields=['content'])
            self.stdout.write(self.style.SUCCESS('[+] Изображения загружены и пути обновлены'))

    def _create_slug(self, title):
        """Создание slug из заголовка с транслитерацией"""
        import re

        # Карта транслитерации
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            ' ': '-', '–': '-', '—': '-', ':': '', '?': '', '!': '', '.': '',
            ',': '', '"': '', "'": '', '«': '', '»': '', '(': '', ')': ''
        }

        title_lower = title.lower()
        translitted = ''
        for char in title_lower:
            translitted += translit_map.get(char, char if char.isalnum() or char == '-' else '')

        # Очистка и нормализация
        slug = re.sub(r'[^\w-]', '', translitted)
        slug = re.sub(r'[-]+', '-', slug)  # Множественные дефисы в один
        slug = slug.strip('-')

        return slug[:200]  # Увеличил лимит для SEO

    def _create_excerpt(self, content):
        """Создание краткого описания из контента"""
        import re

        # Удаляем Markdown разметку
        text = re.sub(r'#.*\n', '', content)  # Заголовки
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Ссылки
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Изображения
        text = re.sub(r'\*\*', '', text)  # Жирный
        text = re.sub(r'\*', '', text)  # Курсив
        text = re.sub(r'\n+', ' ', text)  # Переносы строк

        # Берем первые 200 символов
        excerpt = text.strip()[:200]

        # Обрезаем до последнего предложения
        if '.' in excerpt:
            excerpt = excerpt[:excerpt.rfind('.') + 1]

        return excerpt if excerpt else 'Статья с VC.ru'

    def _optimize_image(self, image_path, max_width=1200, max_height=800, quality=80):
        """Оптимизация обложки статьи с сохранением пропорций"""
        with Image.open(image_path) as img:
            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = rgb_img

            # Масштабируем с сохранением пропорций
            ratio = min(max_width / img.width, max_height / img.height)

            # Уменьшаем только если изображение больше максимальных размеров
            if ratio < 1:
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Сохраняем в байты
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            return output.read()

    def _upload_and_update_images(self, content, article, article_folder, images_info):
        """Загрузка всех изображений в ArticleMedia и обновление путей"""
        import re
        from articles.models import ArticleMedia

        # Создаем словарь: filename -> URL
        image_urls = {}

        # Первое изображение уже загружено как обложка - удаляем его из контента
        if images_info:
            first_filename = images_info[0]['filename']
            # Удаляем первое изображение из контента, чтобы избежать дублирования
            pattern_first = rf'!\[.*?\]\(images/{re.escape(first_filename)}\)\n?'
            content = re.sub(pattern_first, '', content)

        # Загружаем остальные изображения через ArticleMedia
        for idx, img_info in enumerate(images_info[1:], start=2):
            filename = img_info['filename']
            image_path = os.path.join(article_folder, 'images', filename)

            if os.path.exists(image_path):
                self.stdout.write(f'  [{idx}/{len(images_info)}] {filename}')

                # Создаем ArticleMedia объект
                with open(image_path, 'rb') as f:
                    media = ArticleMedia(
                        article=article,
                        media_type='image',
                        title=f'Image {idx}',
                        alt_text=img_info.get('alt', '')[:200],
                        order=idx
                    )
                    media.file.save(filename, ContentFile(f.read()), save=True)
                    image_urls[filename] = media.file.url

        # Заменяем пути в контенте
        pattern = r'!\[(.*?)\]\(images/(.*?)\)'

        def replace_path(match):
            alt = match.group(1)
            filename = match.group(2)
            url = image_urls.get(filename, '')
            return f'![{alt}]({url})' if url else match.group(0)

        updated_content = re.sub(pattern, replace_path, content)
        return updated_content
