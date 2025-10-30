# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from articles.models import Category


class Command(BaseCommand):
    help = 'Добавляет новые категории из VC.ru'

    def handle(self, *args, **options):
        new_categories = [
            {"name": "Право", "icon": "⚖️", "description": "Юридические вопросы"},
            {"name": "Техника", "icon": "🔧", "description": "Гаджеты и техника"},
            {"name": "Маркетплейсы", "icon": "🛍️", "description": "Торговля на маркетплейсах"},
            {"name": "Кейсы роста", "icon": "📊", "description": "Успешные кейсы бизнеса"},
            {"name": "Телеграм", "icon": "💬", "description": "Telegram боты и каналы"},
            {"name": "Транспорт", "icon": "🚗", "description": "Транспорт и логистика"},
            {"name": "Приёмная", "icon": "📺", "description": "Вопросы и ответы"},
            {"name": "Соцсети", "icon": "💕", "description": "Социальные сети"},
            {"name": "SEO", "icon": "🔍", "description": "Поисковая оптимизация"},
            {"name": "Будущее", "icon": "🔮", "description": "Технологии будущего"},
            {"name": "Что почитать", "icon": "📚", "description": "Рекомендации книг"},
            {"name": "Ритейл", "icon": "🏪", "description": "Розничная торговля"},
            {"name": "Офлайн", "icon": "🔘", "description": "Офлайн бизнес"},
            {"name": "Офтоп", "icon": "🎭", "description": "Разное"},
            {"name": "Еда", "icon": "🍴", "description": "Кулинария и рестораны"},
            {"name": "Миграция", "icon": "ℹ️", "description": "Переезд и миграция"},
            {"name": "Трибуна", "icon": "⚔️", "description": "Дискуссии"},
            {"name": "Истории", "icon": "🎪", "description": "Интересные истории"},
            {"name": "Видео", "icon": "▶️", "description": "Видеоконтент"},
            {"name": "ChatGPT", "icon": "🌀", "description": "ChatGPT и AI"},
            {"name": "Вопросы", "icon": "❓", "description": "Вопрос-ответ"},
            {"name": "Будни", "icon": "🌙", "description": "Будни разработчиков"},
            {"name": "Офис", "icon": "🦗", "description": "Офисная жизнь"},
            {"name": "Apple", "icon": "🍎", "description": "Продукты Apple"},
            {"name": "Находки", "icon": "💡", "description": "Интересные находки"},
            {"name": "Конкурсы", "icon": "🎁", "description": "Конкурсы и розыгрыши"},
            {"name": "Midjourney", "icon": "🎨", "description": "Midjourney и генерация"},
        ]

        added = 0
        skipped = 0

        for cat_data in new_categories:
            slug = slugify(cat_data['name'], allow_unicode=True)

            if Category.objects.filter(name=cat_data['name']).exists():
                self.stdout.write(self.style.WARNING(f'[SKIP] {cat_data["name"]} (already exists)'))
                skipped += 1
                continue

            try:
                Category.objects.create(
                    name=cat_data['name'],
                    slug=slug,
                    icon=cat_data['icon'],
                    description=cat_data['description']
                )
                self.stdout.write(self.style.SUCCESS(f'[ADD] {cat_data["name"]}'))
                added += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] {cat_data["name"]}: {str(e)}'))
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(f'  Added: {added}')
        self.stdout.write(f'  Skipped: {skipped}')
        self.stdout.write(f'  Total categories: {Category.objects.count()}')
