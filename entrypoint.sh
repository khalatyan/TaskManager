#!/bin/sh

touch task_manager/__init__.py
echo "⏳ Waiting for Postgres at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "✅ Postgres is up!"

echo "🔁 Running migrations..."
alembic upgrade head

echo "🚀 Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
