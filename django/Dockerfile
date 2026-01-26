# Этап 1: Builder (сборка зависимостей и статики)
FROM python:3.11 as builder

WORKDIR /app

# Копируем requirements
COPY ../requirements/prod.txt /app/requirements.txt  

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . /app/

# Собираем статические файлы 
ENV DJANGO_SETTINGS_MODULE=web_2025.settings
RUN python manage.py collectstatic --noinput

# Этап 2: Production (минимальный образ)
FROM python:3.11-slim

# Создаём непривилегированного пользователя
RUN useradd -m appuser

WORKDIR /app

# Копируем зависимости и код из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Права
RUN chown -R appuser:appuser /app

USER appuser

# ENTRYPOINT и CMD 
ENTRYPOINT ["/app/entrypoint.sh"]  
CMD ["gunicorn", "web_2025.wsgi:application", "--bind", "0.0.0.0:8000"]  