FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем весь проект сразу
COPY . .
COPY alembic alembic
COPY alembic.ini .
COPY task_manager app
COPY entrypoint.sh .

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Даем права на скрипт
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
