"""
Генерация sitemap.xml для поисковых систем
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category, Tag


class ArticleSitemap(Sitemap):
    """Карта сайта для статей"""
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        """Возвращает все опубликованные статьи"""
        return Article.objects.filter(status='published').order_by('-published_at')

    def lastmod(self, obj):
        """Дата последнего изменения"""
        return obj.updated_at

    def location(self, obj):
        """URL статьи"""
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    """Карта сайта для категорий"""
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        """Возвращает все категории с опубликованными статьями"""
        categories = []
        for category in Category.objects.all():
            if category.articles.filter(status='published').exists():
                categories.append(category)
        return categories

    def lastmod(self, obj):
        """Дата последней статьи в категории"""
        latest_article = obj.articles.filter(status='published').order_by('-updated_at').first()
        return latest_article.updated_at if latest_article else obj.created_at

    def location(self, obj):
        """URL категории"""
        return obj.get_absolute_url()


class TagSitemap(Sitemap):
    """Карта сайта для тегов"""
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        """Возвращает все теги с опубликованными статьями"""
        tags = []
        for tag in Tag.objects.all():
            if tag.articles.filter(status='published').exists():
                tags.append(tag)
        return tags

    def lastmod(self, obj):
        """Дата последней статьи с этим тегом"""
        latest_article = obj.articles.filter(status='published').order_by('-updated_at').first()
        return latest_article.updated_at if latest_article else obj.created_at

    def location(self, obj):
        """URL тега"""
        return obj.get_absolute_url()


class StaticPagesSitemap(Sitemap):
    """Карта сайта для статических страниц"""
    changefreq = "monthly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        """Возвращает список статических страниц"""
        return [
            'home',
            'about',
            'contact',
            'privacy',
            'terms',
        ]

    def location(self, item):
        """URL страницы"""
        # Мапинг имен на реальные URL
        url_mapping = {
            'home': reverse('articles:home'),
            'about': reverse('articles:about'),
            'contact': reverse('articles:contact'),
            'privacy': reverse('articles:privacy'),
            'terms': reverse('articles:terms'),
        }
        return url_mapping.get(item, '/')