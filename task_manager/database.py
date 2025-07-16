import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DataBaseConfig:
    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = os.getenv('DB_PORT', 5432)
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'auth_db')

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


config = DataBaseConfig()
DATABASE_URL = config.database_url

# Движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессии
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей
class ORMBase(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

# Dependency для FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
