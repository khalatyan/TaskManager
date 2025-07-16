from fastapi import Depends

from task_manager.users.application.repository import UserRepository
from task_manager.users.exceptions import UserAlreadyExistsError
from task_manager.users.models import User
from task_manager.users.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead, UserAuth, \
    UserFullRead
from task_manager.users.utils import hash_password, verify_password
from task_manager.utils.mixins.interactors import CRUDInteractorMixin


class UserInteractor(CRUDInteractorMixin[User, UserCreate, UserUpdate, UserRead]):
    crud_repository = UserRepository
    enabled_delete = True

    def __init__(
        self,
        crud_repository: UserRepository = Depends(UserRepository)
    ):
        super().__init__(crud_repository)

    async def create(self, schema: UserCreate) -> UserRead:
        existing_users = await self.crud_repository.filter(email=schema.email)
        if existing_users:
            raise UserAlreadyExistsError(schema.email)

        hashed_schema = UserCreateHashedPassword(
            email=schema.email,
            hashed_password=hash_password(schema.password),
        )
        return await self.crud_repository.create(hashed_schema)

    async def authenticate_user(self, user: UserAuth):
        result = await self.crud_repository.filter(
            email=user.email,
            with_schema=UserFullRead
        )
        result_user = result[0] if result else None
        if not result_user or not verify_password(user.password, result_user.hashed_password):
            return None
        return result_user



