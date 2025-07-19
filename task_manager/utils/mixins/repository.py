from abc import ABCMeta
from optparse import Option
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict

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

    async def filter(
            self,
            with_schema: BaseModel = None,
            and_filters: Optional[Dict[str, Any]] = None,
            or_filters: Optional[Dict[str, Any]] = None,
    ) -> List[R]:
        clauses = []

        if and_filters:
            and_expressions = [getattr(self.model, key) == value for key, value in and_filters.items()]
            if and_expressions:
                clauses.append(sa_and(*and_expressions))

        if or_filters:
            or_expressions = [getattr(self.model, key) == value for key, value in or_filters.items()]
            if or_expressions:
                clauses.append(sa_or(*or_expressions))

        if not clauses:
            stmt = select(self.model)
        elif len(clauses) == 1:
            stmt = select(self.model).where(clauses[0])
        else:
            stmt = select(self.model).where(sa_and(*clauses))  # или sa_or, в зависимости от логики

        result = await self.session.execute(stmt)
        objs = result.scalars().all()
        with_schema = with_schema or self.read_schema
        return [with_schema.from_orm(obj) for obj in objs]


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