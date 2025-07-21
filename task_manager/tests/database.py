import os

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from task_manager.database import ORMBase
from task_manager.main import app
from httpx import AsyncClient


class DataBaseConfig:
    """ Конфигурация основного БД. """
    def __init__(self):
        """ init. """
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = os.getenv('DB_PORT', 5432)
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = 'test_database'

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

config = DataBaseConfig()
TEST_DATABASE_URL = config.database_url

engine_test = create_async_engine(TEST_DATABASE_URL, future=True)
AsyncSessionTest = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
async def setup_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(ORMBase.metadata.drop_all)
        await conn.run_sync(ORMBase.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(ORMBase.metadata.drop_all)


@pytest.fixture
async def session(setup_test_db):
    async with AsyncSessionTest() as session:
        yield session


@pytest.fixture
async def async_client(session):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
