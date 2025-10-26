# 📋 Информация о проекте reads.su

## 🌐 Доступы

### Сайт
- **URL**: https://reads.su
- **Админка**: https://reads.su/admin/

### SSH Доступ к серверу
- **IP**: 213.171.5.75
- **Пользователь**: root
- **Пароль**: `p,-iVfmLCQ3EiK`
- **SSH ключ**: `~/.ssh/reads_su_key` (настроен, пароль не требуется)

### База данных PostgreSQL
- **Host**: localhost
- **Port**: 5432
- **Database**: reads_su
- **User**: reads_user
- **Password**: `reads_password_2024_secure`
- **DATABASE_URL**: `postgres://reads_user:reads_password_2024_secure@localhost:5432/reads_su`

---

## 👤 Пользователи

### Администратор
- **Username**: admin
- **Email**: admin@reads.su
- **Password**: `admin123`

### Тестовый пользователь
- **Username**: testuser
- **Email**: test@reads.su
- **Password**: `testpass123`

---

## 🚀 Команды для разработки

### Локальная разработка

#### Запуск сервера разработки
```bash
python manage.py runserver
```

#### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Создание суперпользователя
```bash
python manage.py createsuperuser
```

#### Сбор статических файлов
```bash
python manage.py collectstatic --noinput
```

#### Компрессия статических файлов
```bash
python manage.py compress --force
```

#### Очистка кэша
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

---

## 📦 Деплой на продакшн

### Быстрый деплой (через скрипт)
```bash
./deploy.sh
```

### Полная команда деплоя
```bash
# 1. Push на GitHub
git push origin main

# 2. Деплой на сервер (без пароля, через SSH ключ)
ssh -i ~/.ssh/reads_su_key root@213.171.5.75 "cd /opt/reads-su && git pull origin main && source venv/bin/activate && export DATABASE_URL='postgres://reads_user:reads_password_2024_secure@localhost:5432/reads_su' && export RAILWAY_ENVIRONMENT=production && python manage.py compress --force && python manage.py collectstatic --noinput && systemctl restart reads-su && redis-cli -n 1 FLUSHDB && echo '✅ Деплой завершен успешно!'"
```

### Подключение к серверу по SSH
```bash
# С использованием ключа (пароль не требуется)
ssh -i ~/.ssh/reads_su_key root@213.171.5.75

# Или просто (если настроен ~/.ssh/config)
ssh root@213.171.5.75
```

---

## 🛠️ Полезные команды на сервере

### Проверка статуса сервиса
```bash
systemctl status reads-su
```

### Перезапуск сервиса
```bash
systemctl restart reads-su
```

### Просмотр логов
```bash
journalctl -u reads-su -f
```

### Очистка Redis кэша
```bash
redis-cli -n 1 FLUSHDB
```

### Просмотр последних коммитов
```bash
cd /opt/reads-su && git log --oneline -5
```

---

## 🔧 Git команды

### Стандартный workflow
```bash
# 1. Проверка статуса
git status

# 2. Добавление файлов
git add .

# 3. Коммит
git commit -m "Описание изменений"

# 4. Push на GitHub
git push origin main

# 5. Деплой на сервер
./deploy.sh
```

### Просмотр истории
```bash
git log --oneline -10
```

### Отмена изменений
```bash
# Отмена изменений в файле
git checkout -- <filename>

# Отмена последнего коммита (но сохранить изменения)
git reset --soft HEAD~1
```

---

## 📊 Мониторинг

### Яндекс.Метрика
- **ID счетчика**: 104704355
- **Доступ**: https://metrika.yandex.ru/

### Яндекс.Вебмастер
- **Verification code**: a932c34bcb78e568
- **Доступ**: https://webmaster.yandex.ru/

---

## 📁 Структура проекта

```
reads-su/
├── articles/           # Основное приложение со статьями
├── users/             # Приложение пользователей
├── static/            # Статические файлы (CSS, JS, изображения)
│   └── css/
│       └── style.css  # Основные стили
├── templates/         # HTML шаблоны
│   ├── base.html      # Базовый шаблон
│   ├── articles/      # Шаблоны статей
│   └── users/         # Шаблоны пользователей
├── media/             # Загружаемые файлы (изображения, видео)
├── manage.py          # Django management команды
├── requirements.txt   # Python зависимости
├── deploy.sh          # Скрипт автоматического деплоя
└── PROJECT_INFO.md    # Этот файл
```

---

## 🔐 Безопасность

### SSH ключ
- **Приватный ключ**: `~/.ssh/reads_su_key`
- **Публичный ключ**: `~/.ssh/reads_su_key.pub`
- **Пароль от ключа**: нет (ключ без пароля)

### Важные файлы с паролями
- `.env` - переменные окружения (НЕ коммитить в Git!)
- `settings.py` - настройки Django

---

## 📝 Полезные ссылки

- **GitHub репозиторий**: https://github.com/7981317-dotcom/reads-su
- **Django документация**: https://docs.djangoproject.com/
- **Bootstrap документация**: https://getbootstrap.com/docs/

---

## 🐛 Решение проблем

### Сайт не открывается
```bash
# Проверить статус сервиса
ssh root@213.171.5.75 "systemctl status reads-su"

# Перезапустить сервис
ssh root@213.171.5.75 "systemctl restart reads-su"
```

### Не применяются стили
```bash
# Очистить кэш и пересобрать статику
ssh root@213.171.5.75 "cd /opt/reads-su && source venv/bin/activate && python manage.py compress --force && python manage.py collectstatic --noinput && redis-cli -n 1 FLUSHDB"
```

### Проблемы с базой данных
```bash
# Подключиться к PostgreSQL
ssh root@213.171.5.75 "psql -U reads_user -d reads_su"
```

---

**Дата создания**: 2025-01-20
**Версия**: 1.0
