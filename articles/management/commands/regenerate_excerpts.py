"""
Django management команда для регенерации excerpt всех статей
Использование: python manage.py regenerate_excerpts
"""

from django.core.management.base import BaseCommand
from articles.models import Article


class Command(BaseCommand):
    help = 'Регенерирует excerpt для всех статей, убирая Markdown разметку'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать, что будет изменено, без фактического изменения',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('Режим DRY RUN - статьи не будут изменены'))

        articles = Article.objects.all()
        total_articles = articles.count()
        updated_count = 0

        self.stdout.write(f'\n📝 Обработка {total_articles} статей...\n')

        for article in articles:
            old_excerpt = article.excerpt

            # Очищаем excerpt, чтобы сработала автоматическая генерация
            article.excerpt = ''

            if not dry_run:
                # save() автоматически сгенерирует новый excerpt с очисткой Markdown
                article.save()
                updated_count += 1

            # Показываем прогресс
            if article.excerpt != old_excerpt:
                self.stdout.write(f'  ✓ {article.title[:60]}...')
                if dry_run:
                    self.stdout.write(f'    Старый: {old_excerpt[:80]}...')
                    self.stdout.write(f'    Новый: (будет регенерирован)')
            else:
                self.stdout.write(f'  - {article.title[:60]}... (без изменений)')

        # Итоговая статистика
        if dry_run:
            self.stdout.write(self.style.WARNING(f'\n⚠️  DRY RUN завершен'))
            self.stdout.write(f'Будет обновлено статей: {total_articles}')
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Готово!'))
            self.stdout.write(f'Обновлено статей: {updated_count}')
