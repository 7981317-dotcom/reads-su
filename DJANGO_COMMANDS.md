# 🐍 Django Commands - Шпаргалка

## 📚 Основные команды

### Запуск сервера разработки
```bash
python manage.py runserver
python manage.py runserver 0.0.0.0:8000  # Доступ из локальной сети
```

### Работа с базой данных

#### Создание миграций
```bash
python manage.py makemigrations
python manage.py makemigrations articles  # Для конкретного приложения
```

#### Применение миграций
```bash
python manage.py migrate
python manage.py migrate articles  # Для конкретного приложения
```

#### Откат миграций
```bash
python manage.py migrate articles 0001  # Откат до конкретной миграции
python manage.py migrate articles zero  # Полный откат приложения
```

#### Просмотр миграций
```bash
python manage.py showmigrations
python manage.py showmigrations articles
```

#### SQL для миграций
```bash
python manage.py sqlmigrate articles 0001
```

---

## 👤 Пользователи

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Смена пароля пользователя
```bash
python manage.py changepassword admin
```

---

## 📦 Статические файлы

### Сбор статики
```bash
python manage.py collectstatic
python manage.py collectstatic --noinput  # Без подтверждения
python manage.py collectstatic --clear    # Очистить перед сбором
```

### Компрессия статики (django-compressor)
```bash
python manage.py compress
python manage.py compress --force  # Принудительная компрессия
```

---

## 🗄️ Управление данными

### Django Shell
```bash
python manage.py shell
python manage.py shell_plus  # Если установлен django-extensions
```

### Примеры в shell:
```python
# Импорт моделей
from articles.models import Article, Category
from django.contrib.auth.models import User

# Получить все статьи
Article.objects.all()

# Получить статью по ID
Article.objects.get(id=1)

# Создать статью
article = Article.objects.create(
    title="Заголовок",
    content="Контент",
    author=User.objects.first()
)

# Обновить статью
article.title = "Новый заголовок"
article.save()

# Удалить статью
article.delete()

# Фильтрация
Article.objects.filter(published=True)
Article.objects.filter(author__username='admin')

# Поиск
Article.objects.filter(title__icontains='python')

# Сортировка
Article.objects.order_by('-created_at')

# Агрегация
from django.db.models import Count
Article.objects.aggregate(Count('id'))

# Очистка кэша
from django.core.cache import cache
cache.clear()
```

### Дамп данных (backup)
```bash
# Вся база
python manage.py dumpdata > backup.json

# Конкретное приложение
python manage.py dumpdata articles > articles_backup.json

# С отступами (для читабельности)
python manage.py dumpdata articles --indent 2 > articles.json

# Исключая контент-типы
python manage.py dumpdata --exclude contenttypes --exclude auth.permission > backup.json
```

### Загрузка данных
```bash
python manage.py loaddata backup.json
python manage.py loaddata articles.json
```

---

## 🧹 Очистка и обслуживание

### Очистка сессий
```bash
python manage.py clearsessions
```

### Удаление неиспользуемых файлов
```bash
python manage.py collectstatic --clear --noinput
```

### Проверка проекта
```bash
python manage.py check
python manage.py check --deploy  # Проверка для продакшн
```

---

## 🔍 Отладка и информация

### Показать SQL запросы
```bash
python manage.py dbshell  # Открыть консоль БД
```

### Информация о проекте
```bash
python manage.py diffsettings  # Отличия от дефолтных настроек
python manage.py showmigrations  # Список миграций
```

### Тестирование
```bash
python manage.py test
python manage.py test articles  # Тесты конкретного приложения
python manage.py test articles.tests.TestArticle  # Конкретный тест
```

---

## 🛠️ Кастомные команды (для reads.su)

### Регенерация excerpt для статей
```bash
python manage.py regenerate_excerpts
python manage.py regenerate_excerpts --dry-run  # Без сохранения
```

---

## 📊 Полезные команды для продакшн

### Проверка перед деплоем
```bash
python manage.py check --deploy
python manage.py test
python manage.py collectstatic --noinput
python manage.py compress --force
```

### Мониторинг
```bash
# Просмотр активных соединений
python manage.py shell
>>> from django.db import connection
>>> connection.queries

# Статистика БД
python manage.py dbshell
\dt  # Список таблиц (PostgreSQL)
\d+ articles_article  # Структура таблицы
```

---

## 🔐 Безопасность

### Генерация нового SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Проверка безопасности
```bash
python manage.py check --deploy
```

---

## 📝 Логирование

### Запуск с детальными логами
```bash
python manage.py runserver --verbosity 3
```

### Уровни verbosity:
- `0` - минимум
- `1` - нормально (по умолчанию)
- `2` - многословно
- `3` - очень многословно

---

## 🎯 Быстрые команды для reads.su

```bash
# Полный цикл разработки
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
python manage.py compress --force && \
python manage.py runserver

# Подготовка к деплою
python manage.py check --deploy && \
python manage.py test && \
python manage.py collectstatic --noinput && \
python manage.py compress --force

# Резервное копирование
python manage.py dumpdata --exclude contenttypes --exclude auth.permission --indent 2 > backup_$(date +%Y%m%d_%H%M%S).json

# Очистка кэша через shell
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Cache cleared')"
```

---

**Документация Django**: https://docs.djangoproject.com/
