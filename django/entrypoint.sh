#!/bin/bash
set -e

#echo "DEBUG: Current directory: $(pwd)"
#echo "DEBUG: PYTHONPATH: $PYTHONPATH"
#echo "DEBUG: Trying to import wsgi..."
#python -c "import web_2025.wsgi" && echo "WSGI import OK" || echo "WSGI import FAILED"
#ls -la /app/web_2025/


echo "Waiting for PostgreSQL..."

max_attempts=30
attempt=1

conn_string="postgresql://$DB_USER:$DB_PASSWORD@db:5432/$DB_NAME"

#echo $conn_string

while [ $attempt -le $max_attempts ]; do
    if python -c "
import psycopg2
try:
    conn = psycopg2.connect('$conn_string')
    conn.close()
    print('Connection successful')
    exit(0)
except Exception as e:
    print('Connection failed:', str(e))
    exit(1)
" ; then
        echo "Postgres is up and accepting connections - continuing"
        break
    else
        echo "Postgres is unavailable - sleeping ($attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "Postgres did not become available after $max_attempts attempts"
    exit 1
fi


echo "Running migrations and collectstatic..."
python web_2025/manage.py migrate
python web_2025/manage.py collectstatic --noinput || true

echo "Starting application..."
exec "$@"
