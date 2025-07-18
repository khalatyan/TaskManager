from typing import TypeVar, Generic, List, Optional, Dict, Any

from fastapi import Depends
from pydantic import BaseModel

from task_manager.utils.mixins.repository import CRUDRepositoryMixin

T = TypeVar("T")  # ORM модель
C = TypeVar("C", bound=BaseModel)  # схема создания (Pydantic)
U = TypeVar("U", bound=BaseModel)  # схема обновления (Pydantic)
R = TypeVar("R", bound=BaseModel)  # схема для чтения (Pydantic)

class CRUDInteractorMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        enabled_create = namespace.get("enabled_create", True)
        enabled_update = namespace.get("enabled_update", True)
        enabled_delete = namespace.get("enabled_delete", True)

        if not enabled_create:
            namespace.pop("create", None)
        if not enabled_update:
            namespace.pop("update", None)
        if not enabled_delete:
            namespace.pop("delete", None)

        return super().__new__(cls, name, bases, namespace)


class CRUDInteractorMixin(Generic[T, C, U, R], metaclass=CRUDInteractorMeta):
    enabled_create: bool = True
    enabled_update: bool = True
    enabled_delete: bool = True

    def __init__(self, crud_repository: CRUDRepositoryMixin):
        self.crud_repository = crud_repository

    async def get_by_id(self, obj_id: int) -> R:
        return await self.crud_repository.get_by_id(obj_id)

    async def create(self, schema: C) -> R:
        return await self.crud_repository.create(schema)

    async def filter(
        self,
        and_filters: Optional[Dict[str, Any]] = None,
        or_filters: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        return await self.crud_repository.filter(and_filters=and_filters, or_filters=or_filters)

    async def update(self, db_obj_id: int, schema: U) -> R:
        return await self.crud_repository.update(db_obj_id, schema)

    async def delete(self, db_obj_id: int):
        return await self.crud_repository.delete(db_obj_id)
