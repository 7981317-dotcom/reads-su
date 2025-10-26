"""
RSS/Atom фиды для статей
"""
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from .models import Article


class LatestArticlesFeed(Feed):
    """RSS-фид последних статей"""
    title = "Reads.su - Последние статьи"
    link = "/"
    description = "Свежие и актуальные статьи на Reads.su"

    def items(self):
        """Возвращает последние 20 опубликованных статей"""
        return Article.objects.filter(
            status='published'
        ).select_related('author', 'category').order_by('-published_at')[:20]

    def item_title(self, item):
        """Заголовок статьи"""
        return item.title

    def item_description(self, item):
        """Описание статьи"""
        return item.excerpt or item.content[:200]

    def item_link(self, item):
        """Ссылка на статью"""
        return reverse('article_detail', args=[item.slug])

    def item_pubdate(self, item):
        """Дата публикации"""
        return item.published_at

    def item_author_name(self, item):
        """Имя автора"""
        return item.author.username if item.author else 'Редакция'

    def item_categories(self, item):
        """Категории и теги"""
        categories = [item.category.name] if item.category else []
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags

    def item_enclosure_url(self, item):
        """URL обложки статьи для RSS"""
        if item.cover:
            return item.cover.url
        return None

    def item_enclosure_length(self, item):
        """Размер файла обложки"""
        if item.cover:
            try:
                return item.cover.size
            except:
                return 0
        return 0

    def item_enclosure_mime_type(self, item):
        """MIME-тип обложки"""
        return "image/jpeg"


class LatestArticlesAtomFeed(LatestArticlesFeed):
    """Atom-фид последних статей"""
    feed_type = Atom1Feed
    subtitle = LatestArticlesFeed.description
