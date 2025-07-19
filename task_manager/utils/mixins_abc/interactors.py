from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel

T = TypeVar("T")  # ORM-модель
C = TypeVar("C", bound=BaseModel)  # Pydantic-схема создания
U = TypeVar("U", bound=BaseModel)  # Pydantic-схема обновления
R = TypeVar("R", bound=BaseModel)  # Pydantic-схема ответа (read)

class AbstractCRUDInteractor(ABC, Generic[T, C, U, R]):
    """
    Абстрактный интерфейс для бизнес-логики CRUD-операций.
    Предполагается, что реализация делегирует действия репозиторию,
    но может содержать дополнительную валидацию или бизнес-логику.
    """

    enabled_create: bool = True
    enabled_update: bool = True
    enabled_delete: bool = True

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> R:
        """
        Получить объект по ID.

        :param obj_id: Идентификатор объекта.
        :return: Объект в виде схемы для чтения.
        """
        ...

    @abstractmethod
    async def create(self, schema: C) -> R:
        """
        Создать новый объект.

        :param schema: Данные для создания.
        :return: Созданный объект.
        """
        ...

    @abstractmethod
    async def filter(
        self,
        and_filters: Optional[Dict[str, Any]] = None,
        or_filters: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        """
        Получить список объектов по AND/OR фильтрам.

        :param and_filters: Условия, объединяемые через AND.
        :param or_filters: Условия, объединяемые через OR.
        :return: Список объектов, удовлетворяющих условиям.
        """
        ...

    @abstractmethod
    async def update(self, db_obj_id: int, schema: U) -> R:
        """
        Обновить объект по ID.

        :param db_obj_id: ID обновляемого объекта.
        :param schema: Данные для обновления.
        :return: Обновлённый объект.
        """
        ...

    @abstractmethod
    async def delete(self, db_obj_id: int) -> None:
        """
        Удалить объект по ID.

        :param db_obj_id: ID объекта для удаления.
        :return: None
        """
        ...
