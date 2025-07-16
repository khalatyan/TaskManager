FROM python:3.11-slim

WORKDIR /task_manager

# Устанавливаем Poetry
RUN pip install poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем без venv и с dev-зависимостями (где uvicorn)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --with dev

# Копируем остальное
COPY alembic alembic
COPY alembic.ini .
COPY task_manager app
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD ["sh", "./entrypoint.sh"]
