#!/bin/sh
echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting app..."
exec poetry run uvicorn task_manager.main:app --host 0.0.0.0 --port 8000
