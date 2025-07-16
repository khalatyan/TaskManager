from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")
C = TypeVar("C")
U = TypeVar("U")


class CRUDMeta(type):
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


class CRUDMixin(Generic[T, C, U], metaclass=CRUDMeta):
    model: Type[T]
    enabled_create: bool = True
    enabled_update: bool = True
    enabled_delete: bool = True

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, obj_id: int) -> T | None:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalars().first()

    async def create(self, schema: C) -> T:
        obj = self.model(**schema.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, db_obj: T, schema: U) -> T:
        data = schema.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: T):
        await self.session.delete(db_obj)
        await self.session.commit()
