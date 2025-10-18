"""
Template tags для обработки Markdown
"""
from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """
    Конвертирует Markdown в HTML с поддержкой:
    - Заголовков (H1-H6)
    - Списков
    - Блоков кода с подсветкой
    - Ссылок
    - Жирного/курсивного текста
    """
    if not text:
        return ''

    # Настройки Markdown с расширениями
    extensions = [
        'markdown.extensions.fenced_code',  # Поддержка блоков кода ```
        'markdown.extensions.codehilite',   # Подсветка синтаксиса
        'markdown.extensions.tables',       # Таблицы
        'markdown.extensions.nl2br',        # Переносы строк
        'markdown.extensions.sane_lists',   # Правильные списки
        'markdown.extensions.toc',          # Оглавление (Table of Contents)
    ]

    extension_configs = {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': False,
        },
        'markdown.extensions.toc': {
            'permalink': False,
            'toc_depth': '2-3',
        }
    }

    # Конвертируем Markdown в HTML
    html = md.markdown(
        text,
        extensions=extensions,
        extension_configs=extension_configs
    )

    return mark_safe(html)
