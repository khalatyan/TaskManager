from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from task_manager.database import ORMBase, DataBaseConfig
from task_manager.database import config as db_config
from task_manager.core.models import User
from task_manager.tasks.models import Task

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

db_config = DataBaseConfig()
config.set_main_option('sqlalchemy.url', db_config.database_url)


def run_migrations_offline():
    context.configure(
        url=db_config.database_url,
        target_metadata=ORMBase.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=ORMBase.metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": db_config.database_url
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())