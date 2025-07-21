from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict
from pydantic import BaseModel

T = TypeVar("T")  # ORM-модель SQLAlchemy
C = TypeVar("C", bound=BaseModel)  # Pydantic-схема для создания объекта
U = TypeVar("U", bound=BaseModel)  # Pydantic-схема для обновления объекта
R = TypeVar("R", bound=BaseModel)  # Pydantic-схема для возврата объекта (read)

class AbstractCRUDRepository(ABC, Generic[T, C, U, R]):
    """
    Абстрактный базовый класс для CRUD-репозитория.
    Определяет интерфейс для стандартных операций с базой данных:
    получение, фильтрация, создание, обновление и удаление объектов.
    """

    model: Type[T]  # ORM-модель, с которой работает репозиторий
    read_schema: Type[R]  # Pydantic-схема, используемая для возврата данных клиенту

    @abstractmethod
    async def get_by_id(self, obj_id: int, with_schema: Optional[BaseModel] = None) -> Optional[R]:
        """
        Получить объект по его ID.

        :param obj_id: Идентификатор объекта.
        :param with_schema: Альтернативная Pydantic-схема для сериализации результата (по умолчанию используется read_schema).
        :return: Объект в виде Pydantic-схемы или None, если не найден.
        """
        ...

    @abstractmethod
    async def filter(
        self,
        with_schema: Optional[Type[BaseModel]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        """
        Получить список объектов по фильтру. Поддерживает фильтрацию с использованием AND и/или OR условий.

        :param filters: Словарь условий.
        :param with_schema: Альтернативная Pydantic-схема для сериализации.
        :return: Список объектов, удовлетворяющих условиям фильтрации.
        """
        ...

    @abstractmethod
    async def create(self, schema: C, with_schema: Optional[BaseModel] = None) -> R:
        """
        Создать новый объект в базе данных.

        :param schema: Pydantic-схема с данными для создания.
        :param with_schema: Альтернативная Pydantic-схема для возврата результата.
        :return: Созданный объект в виде схемы для чтения.
        """
        ...

    @abstractmethod
    async def update(self, db_obj_id: int, schema: U, with_schema: Optional[BaseModel] = None) -> R:
        """
        Обновить существующий объект в базе данных.

        :param db_obj_id: ID обновляемого объекта.
        :param schema: Pydantic-схема с данными для обновления (частичное обновление).
        :param with_schema: Альтернативная Pydantic-схема для возврата результата.
        :return: Обновлённый объект в виде схемы для чтения.
        """
        ...

    @abstractmethod
    async def delete(self, db_obj_id: int) -> None:
        """
        Удалить объект по его ID.

        :param db_obj_id: ID объекта, который нужно удалить.
        :return: None
        """
        ...
