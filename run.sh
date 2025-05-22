#!/bin/bash
# Скрипт для быстрого запуска проекта Django на macOS
set -e

cd "$(dirname "$0")/backend"

# 1. Создать виртуальное окружение, если не существует
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 3. Применить миграции
python manage.py migrate

# 4. Запустить сервер
python manage.py runserver
