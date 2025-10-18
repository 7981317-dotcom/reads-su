#!/bin/bash

# Скрипт деплоя для Timeweb Cloud
# Автоматически выполняется при каждом git push

echo "=== Начало деплоя reads.su ==="

# 1. Установка зависимостей
echo "[1/5] Установка Python зависимостей..."
pip install -r requirements.txt --no-cache-dir

# 2. Сбор статических файлов
echo "[2/5] Сбор статических файлов..."
python manage.py collectstatic --noinput

# 3. Применение миграций базы данных
echo "[3/5] Применение миграций..."
python manage.py migrate --noinput

# 4. Создание кеша (опционально)
echo "[4/5] Очистка кеша..."
python manage.py clear_cache || true

# 5. Перезапуск uWSGI
echo "[5/5] Перезапуск сервера..."
touch /tmp/uwsgi-reload.txt

echo "=== Деплой завершен успешно! ==="
echo "Сайт доступен по адресу: https://reads.su"
