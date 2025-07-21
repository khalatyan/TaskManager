from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel

# Типы для обобщённого интерфейса
T = TypeVar("T")  # ORM-модель (например, User)
C = TypeVar("C", bound=BaseModel)  # Схема для создания (Create)
U = TypeVar("U", bound=BaseModel)  # Схема для обновления (Update)
R = TypeVar("R", bound=BaseModel)  # Схема для чтения (Read)

class AbstractCRUDController(ABC, Generic[T, C, U, R]):
    """
    Абстрактный контроллер для стандартных CRUD-операций.
    Подходит для использования в слоях приложения, где нужно строго задать поведение.
    """

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> R:
        """
        Получить объект по его ID.

        :param obj_id: Идентификатор объекта в базе данных.
        :return: Схема для отображения (read schema).
        """
        pass

    @abstractmethod
    async def create(self, schema: C) -> R:
        """
        Создать новый объект.

        :param schema: Схема с данными для создания (create schema).
        :return: Созданный объект в виде схемы для отображения.
        """
        pass

    @abstractmethod
    async def filter(self, filters: Optional[Dict[str, Any]] = None) -> List[R]:
        """
        Получить список объектов по фильтрам.

        :param filters: Словарь с фильтрами, где ключ — имя поля, значение — условие.
        :return: Список объектов, удовлетворяющих фильтру.
        """
        pass

    @abstractmethod
    async def update(self, db_obj_id: int, schema: U) -> R:
        """
        Обновить объект по его ID.

        :param db_obj_id: Идентификатор объекта, который нужно обновить.
        :param schema: Схема с данными для обновления (update schema).
        :return: Обновлённый объект.
        """
        pass

    @abstractmethod
    async def delete(self, db_obj_id: int) -> None:
        """
        Удалить объект по его ID.

        :param db_obj_id: Идентификатор объекта, который нужно удалить.
        :return: None
        """
        pass
