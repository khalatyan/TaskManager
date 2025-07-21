from abc import ABCMeta
from optparse import Option
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict, Union

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import and_ as sa_and, or_ as sa_or
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from task_manager.database import get_session
from task_manager.utils.mixins_abc.repositories import AbstractCRUDRepository

T = TypeVar("T")
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class CRUDRepositoryMeta(ABCMeta):
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


class CRUDRepositoryMixin(AbstractCRUDRepository, Generic[T, C, U, R], metaclass=CRUDRepositoryMeta):
    model: Type[T]
    read_schema: Type[R]
    enabled_create: bool = True
    enabled_update: bool = True
    enabled_delete: bool = True

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_by_id(self, obj_id: int, with_schema: BaseModel = None) -> R | None:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalars().first()
        with_schema = with_schema or self.read_schema
        return with_schema.from_orm(obj)

    def _build_filter_clause(self, filters: Union[Dict, List]) -> Any:
        """
        Рекурсивно строит SQLAlchemy выражение из вложенных фильтров
        """
        if isinstance(filters, list):
            # просто список условий
            return sa_and(*[self._build_filter_clause(f) for f in filters])

        if isinstance(filters, dict):
            if "and" in filters:
                return sa_and(*[self._build_filter_clause(f) for f in filters["and"]])
            if "or" in filters:
                return sa_or(*[self._build_filter_clause(f) for f in filters["or"]])

            return sa_and(*[
                getattr(self.model, field) == value
                for field, value in filters.items()
            ])

        raise ValueError("Invalid filter structure")

    async def filter(
        self,
        with_schema: Optional[Type[BaseModel]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        stmt = select(self.model)

        if filters:
            clause = self._build_filter_clause(filters)
            stmt = stmt.where(clause)

        result = await self.session.execute(stmt)
        objs = result.scalars().all()

        schema = with_schema or self.read_schema
        return [schema.from_orm(obj) for obj in objs]


    async def create(self, schema: C, with_schema: BaseModel = None) -> R:
        obj = self.model(**schema.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        with_schema = with_schema or self.read_schema
        return with_schema.from_orm(obj)

    async def update(self, db_obj_id: int, schema: U, with_schema: BaseModel = None) -> R:
        result = await self.session.execute(select(self.model).where(self.model.id == db_obj_id))
        db_obj = result.scalars().first()
        data = schema.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        with_schema = with_schema or self.read_schema
        return with_schema.from_orm(db_obj)

    async def delete(self, db_obj_id: int):
        result = await self.session.execute(select(self.model).where(self.model.id == db_obj_id))
        db_obj = result.scalars().first()
        await self.session.delete(db_obj)
        await self.session.commit()