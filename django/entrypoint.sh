#!/bin/bash

# Ждём БД
until pg_isready -h db -p 5432 -U ${DB_USER}; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Миграции и статика 
python manage.py migrate
python manage.py collectstatic --noinput

# Запуск основного процесса
exec "$@"