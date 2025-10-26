"""
Template tags для обработки Markdown
"""
from django import template
from django.utils.safestring import mark_safe
import markdown as md
import re

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
    - Изображений с размытым фоном
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

    # Добавляем background-image к контейнерам изображений для эффекта blur
    # Ищем <p><img src="..." alt="..."></p> и добавляем style с background-image
    def add_bg_image(match):
        img_tag = match.group(1)
        # Извлекаем URL изображения из тега img
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if src_match:
            img_url = src_match.group(1)
            return f'<p style="background-image: url(\'{img_url}\');">{img_tag}</p>'
        return match.group(0)

    html = re.sub(r'<p>(<img[^>]+>)</p>', add_bg_image, html)

    return mark_safe(html)
