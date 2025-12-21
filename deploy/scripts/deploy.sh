#!/bin/bash

set -e  # Остановка при любой ошибке

echo "=== Начало деплоя FEFU Lab ==="

# === Конфигурируемые переменные ===
REPO_URL="https://github.com/cuteghostcat/web_fefu_2025.git"
PROJECT_DIR="/var/www/fefu_lab/web_fefu_2025"
VENV_DIR="$PROJECT_DIR/venv"
DJANGO_DIR="$PROJECT_DIR/web_2025"
DB_PASSWORD="ghostpass"  # Лучше потом убрать и вводить вручную, но для лабы можно оставить

# === 1. Клонируем или обновляем репозиторий ===
if [ -d "$PROJECT_DIR" ]; then
    echo "Обновляем существующий репозиторий..."
    cd $PROJECT_DIR
    git pull
else
    echo "Клонируем репозиторий..."
    sudo mkdir -p $PROJECT_DIR
    sudo chown -R $USER:$USER $PROJECT_DIR
    git clone "$REPO_URL" $PROJECT_DIR
    cd $PROJECT_DIR
fi

# === 2. Устанавливаем системные пакеты (если нужно) ===
sudo apt update
sudo apt install -y python3-venv python3-pip git nginx postgresql postgresql-contrib

# === 3. Виртуальное окружение и зависимости Python ===
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# === 4. Логи и права ===
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo mkdir -p $DJANGO_DIR/static $DJANGO_DIR/media $DJANGO_DIR/staticfiles
sudo chown -R www-data:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR

# === 5. Копируем конфиги сервисов ===
sudo cp deploy/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
sudo cp deploy/nginx/fefu_lab.conf /etc/nginx/sites-available/fefu_lab.conf
sudo ln -sf /etc/nginx/sites-available/fefu_lab.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# === 6. Миграции, загрузка данных, статика ===
cd "$DJANGO_DIR"
source $VENV_DIR/bin/activate
python manage.py dumpdata --indent 2 --output /tmp/data1.json
python manage.py migrate
#python manage.py loaddata data.json || echo "data.json не найден — пропускаем"
python manage.py loaddata /tmp/data1.json || echo "data1.json не найден — пропускаем"
python manage.py collectstatic --noinput
deactivate

# === 7. Перезапускаем сервисы ===
sudo systemctl daemon-reload
sudo systemctl restart gunicorn nginx
sudo systemctl enable gunicorn nginx

# === 8. Проверка доступности ===
echo "Проверяем приложение..."
if curl -f http://localhost:80 > /dev/null; then
    echo "=== Деплой успешно завершён! ==="
    echo "Приложение доступно по адресу: http://$(hostname -I | awk '{print $1}')"
else
    echo "ОШИБКА: Приложение не отвечает на http://localhost:80"
    exit 1
fi