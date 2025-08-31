#!/bin/sh

# echo "Waiting for postgres..."
# while ! nc -z db 5432; do
#   sleep 0.5
# done
# echo "PostgreSQL started"

# echo "Waiting for redis..."
# while ! nc -z redis 6379; do
#   sleep 0.5
# done
# echo "Redis started"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start server
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
