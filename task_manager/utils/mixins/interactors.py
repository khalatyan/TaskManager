from typing import TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

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
    crud_repository: CRUDRepositoryMixin = None

    def __init__(self, session: AsyncSession):
        self.session = session
        self.crud_repository = self.crud_repository(session)

    async def get_by_id(self, obj_id: int) -> R:
        return await self.crud_repository.get_by_id(obj_id)

    async def create(self, schema: C) -> R:
        return await self.crud_repository.create(schema)

    async def update(self, db_obj_id: int, schema: U) -> R:
        return await self.crud_repository.update(db_obj_id, schema)

    async def delete(self, db_obj_id: int):
        return await self.crud_repository.delete(db_obj_id)
