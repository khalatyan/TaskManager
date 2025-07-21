from abc import ABCMeta
from typing import TypeVar, Generic, List, Optional, Dict, Any

from pydantic import BaseModel

from task_manager.utils.mixins.interactors import CRUDInteractorMixin
from task_manager.utils.mixins.repository import CRUDRepositoryMixin
from task_manager.utils.mixins_abc.controllers import AbstractCRUDController
from task_manager.utils.mixins_abc.interactors import AbstractCRUDInteractor

T = TypeVar("T")
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)

class CRUDControllerMeta(ABCMeta):  # Наследуемся от ABCMeta, а не просто от type
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


class CRUDControllerMixin(AbstractCRUDController, Generic[T, C, U, R], metaclass=CRUDControllerMeta):
    enabled_create: bool = True
    enabled_update: bool = True
    enabled_delete: bool = True

    def __init__(self, crud_interactor: CRUDInteractorMixin):
        self.crud_interactor = crud_interactor

    async def get_by_id(self, obj_id: int) -> R:
        return await self.crud_interactor.get_by_id(obj_id)

    async def create(self, schema: C) -> R:
        return await self.crud_interactor.create(schema)

    async def filter(
        self,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        return await self.crud_interactor.filter(filters=filters)

    async def update(self, db_obj_id: int, schema: U) -> R:
        return await self.crud_interactor.update(db_obj_id, schema)

    async def delete(self, db_obj_id: int):
        return await self.crud_interactor.delete(db_obj_id)
