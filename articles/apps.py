from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        """Импорт сигналов при запуске приложения"""
        import articles.signals  # noqa
