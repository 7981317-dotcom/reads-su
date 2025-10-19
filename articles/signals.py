"""
Сигналы для сброса кеша при изменении данных
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Article, Category, Tag
from comments.models import Comment


@receiver([post_save, post_delete], sender=Article)
def clear_article_cache(sender, **kwargs):
    """Сброс кеша при изменении статей"""
    cache.delete('popular_articles')
    cache.delete('categories_with_count')
    cache.delete('popular_tags')


@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, **kwargs):
    """Сброс кеша при изменении категорий"""
    cache.delete('categories_with_count')


@receiver([post_save, post_delete], sender=Tag)
def clear_tag_cache(sender, **kwargs):
    """Сброс кеша при изменении тегов"""
    cache.delete('popular_tags')


@receiver([post_save, post_delete], sender=Comment)
def clear_comment_cache(sender, **kwargs):
    """Сброс кеша при изменении комментариев"""
    cache.delete('popular_comments')
