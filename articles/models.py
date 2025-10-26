from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify  # Используем python-slugify для транслитерации
from django.utils import timezone
from django.utils.html import strip_tags
import re
from .utils.image_optimizer import optimize_image, optimize_icon


def create_slug(text):
    """Создает slug с транслитерацией кириллицы в латиницу"""
    # slugify автоматически транслитерирует с помощью unidecode
    slug = slugify(text)
    if not slug:
        # Если slug пустой, генерируем из хэша
        slug = f"slug-{hash(text) % 100000}"
    return slug


class Category(models.Model):
    """Категория статей"""
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка (emoji)', max_length=10, blank=True, default='📁')
    icon_image = models.ImageField('Изображение иконки', upload_to='categories/icons/', blank=True, null=True)
    color = models.CharField('Цвет', max_length=7, default='#3B82F6', help_text='HEX цвет')
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)

        # Оптимизация иконки категории
        if self.icon_image:
            try:
                # Проверяем, что это новое изображение
                if not self.pk or self._state.adding:
                    self.icon_image = optimize_icon(self.icon_image, size=200, quality=90)
                else:
                    # Проверяем, изменилось ли изображение
                    try:
                        old_instance = Category.objects.get(pk=self.pk)
                        if old_instance.icon_image != self.icon_image:
                            self.icon_image = optimize_icon(self.icon_image, size=200, quality=90)
                    except Category.DoesNotExist:
                        self.icon_image = optimize_icon(self.icon_image, size=200, quality=90)
            except Exception as e:
                # Если оптимизация не удалась, просто сохраняем оригинал
                print(f"Ошибка оптимизации иконки категории: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:category', kwargs={'slug': self.slug})

    def article_count(self):
        return self.articles.filter(status='published').count()


class Tag(models.Model):
    """Тег статьи"""
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('URL', max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:tag', kwargs={'slug': self.slug})

    def article_count(self):
        return self.articles.filter(status='published').count()


class Article(models.Model):
    """Статья"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    ]

    # Основная информация
    title = models.CharField('Заголовок', max_length=250)
    slug = models.SlugField('URL', max_length=250, unique=True, blank=True)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)

    # Содержание
    content = models.TextField('Содержание')
    excerpt = models.TextField('Краткое описание', max_length=500, blank=True,
                                help_text='Краткое описание для превью (до 500 символов)')

    # Обложка
    cover_image = models.ImageField('Обложка (изображение)', upload_to='articles/covers/%Y/%m/', blank=True, null=True)
    cover_video = models.FileField('Обложка (видео)', upload_to='articles/covers/videos/%Y/%m/', blank=True, null=True,
                                    help_text='Видео обложка (mp4, webm). Если указано, будет использоваться вместо изображения')
    cover_video_url = models.CharField('Обложка (видео по URL)', max_length=500, blank=True,
                                        help_text='URL видео или YouTube (например: https://www.youtube.com/watch?v=... или youtube:VIDEO_ID)')
    cover_alt = models.CharField('Alt текст обложки', max_length=200, blank=True)

    # Связи
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles',
                                verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                  related_name='articles', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='articles', verbose_name='Теги', blank=True)

    # Статус и даты
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    published_at = models.DateTimeField('Опубликовано', null=True, blank=True)

    # Статистика
    views_count = models.PositiveIntegerField('Просмотры', default=0)
    likes_count = models.PositiveIntegerField('Лайки', default=0)
    comments_count = models.PositiveIntegerField('Комментарии', default=0)

    # SEO
    meta_title = models.CharField('SEO заголовок', max_length=70, blank=True)
    meta_description = models.CharField('SEO описание', max_length=160, blank=True)

    # Настройки
    featured = models.BooleanField('Избранное', default=False,
                                    help_text='Отображать на главной странице')
    allow_comments = models.BooleanField('Разрешить комментарии', default=True)
    is_pinned = models.BooleanField('Закреплено', default=False)
    pin_order = models.PositiveIntegerField('Порядок закрепления', default=0,
                                             help_text='Порядок отображения закрепленной статьи (1 - вверху, 2 - второй и т.д.). 0 - не закреплено')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-is_pinned', 'pin_order', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]

    def save(self, *args, **kwargs):
        # Генерация slug из заголовка с транслитерацией
        if not self.slug:
            self.slug = create_slug(self.title)

        # Оптимизация обложки статьи с сохранением пропорций
        if self.cover_image:
            try:
                # Проверяем, что это новое изображение
                if not self.pk or self._state.adding:
                    self.cover_image = optimize_image(self.cover_image, max_width=1200, max_height=800, quality=85, crop=False)
                else:
                    # Проверяем, изменилось ли изображение
                    try:
                        old_instance = Article.objects.get(pk=self.pk)
                        if old_instance.cover_image != self.cover_image:
                            self.cover_image = optimize_image(self.cover_image, max_width=1200, max_height=800, quality=85, crop=False)
                    except Article.DoesNotExist:
                        self.cover_image = optimize_image(self.cover_image, max_width=1200, max_height=800, quality=85, crop=False)
            except Exception as e:
                # Если оптимизация не удалась, просто сохраняем оригинал
                print(f"Ошибка оптимизации обложки статьи: {e}")

        # Автоматическая генерация excerpt из content
        if not self.excerpt and self.content:
            # Очистка HTML тегов и iframe из контента
            clean_content = self.content

            # Удаляем HTML теги (включая iframe, div, и т.д.)
            clean_content = re.sub(r'<[^>]+>', '', clean_content)

            # Удаляем markdown ссылки на изображения ![alt](url)
            clean_content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', clean_content)

            # Удаляем markdown ссылки [text](url)
            clean_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_content)

            # Удаляем markdown жирный текст **text** или __text__
            clean_content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', clean_content)
            clean_content = re.sub(r'__([^_]+)__', r'\1', clean_content)

            # Удаляем markdown курсив *text* или _text_
            clean_content = re.sub(r'\*([^\*]+)\*', r'\1', clean_content)
            clean_content = re.sub(r'_([^_]+)_', r'\1', clean_content)

            # Удаляем markdown заголовки (#, ##, ###)
            clean_content = re.sub(r'^#+\s+', '', clean_content, flags=re.MULTILINE)

            # Удаляем множественные пробелы и переносы строк
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()

            # Берём первые 300 символов
            self.excerpt = clean_content[:300] + '...' if len(clean_content) > 300 else clean_content

        # Установка даты публикации
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        # Генерация SEO полей
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160] if self.excerpt else ''

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def reading_time(self):
        """Расчет времени чтения"""
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count / words_per_minute
        return max(1, round(minutes))

    def increment_views(self):
        """Увеличение счетчика просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ArticleView(models.Model):
    """Просмотры статьи (для детальной статистики)"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.CharField('User Agent', max_length=300, blank=True)
    viewed_at = models.DateTimeField('Дата просмотра', auto_now_add=True)

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['article', '-viewed_at']),
        ]

    def __str__(self):
        return f'{self.article.title} - {self.viewed_at}'


class Reaction(models.Model):
    """Реакции на статью (лайки, закладки)"""
    REACTION_TYPES = [
        ('like', 'Лайк'),
        ('bookmark', 'Закладка'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField('Тип реакции', max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Реакция'
        verbose_name_plural = 'Реакции'
        unique_together = ['article', 'user', 'reaction_type']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'reaction_type']),
            models.Index(fields=['user', 'reaction_type']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.get_reaction_type_display()} - {self.article.title}'


class ArticleMedia(models.Model):
    """Медиа-файлы для встраивания в контент статей"""
    MEDIA_TYPES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='media_files', verbose_name='Статья')
    media_type = models.CharField('Тип медиа', max_length=10, choices=MEDIA_TYPES, default='image')
    file = models.FileField('Файл', upload_to='articles/media/%Y/%m/')
    title = models.CharField('Название', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    alt_text = models.CharField('Alt текст', max_length=200, blank=True, help_text='Для изображений')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Загружено', auto_now_add=True)

    class Meta:
        verbose_name = 'Медиа-файл'
        verbose_name_plural = 'Медиа-файлы'
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        # Оптимизация изображений в контенте
        if self.media_type == 'image' and self.file:
            try:
                # Проверяем, что это новое изображение
                if not self.pk or self._state.adding:
                    self.file = optimize_image(self.file, max_width=1920, max_height=1080, quality=85)
                else:
                    # Проверяем, изменилось ли изображение
                    try:
                        old_instance = ArticleMedia.objects.get(pk=self.pk)
                        if old_instance.file != self.file:
                            self.file = optimize_image(self.file, max_width=1920, max_height=1080, quality=85)
                    except ArticleMedia.DoesNotExist:
                        self.file = optimize_image(self.file, max_width=1920, max_height=1080, quality=85)
            except Exception as e:
                # Если оптимизация не удалась, просто сохраняем оригинал
                print(f"Ошибка оптимизации медиа-файла: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_media_type_display()} - {self.article.title}'

    @property
    def file_url(self):
        """Получить URL файла"""
        return self.file.url if self.file else ''
