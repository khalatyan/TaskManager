from task_manager.users.application.repository import UserRepository
from task_manager.users.exceptions import UserAlreadyExistsError
from task_manager.users.models import User
from task_manager.users.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead
from task_manager.users.utils import hash_password
from task_manager.utils.mixins.interactors import CRUDInteractorMixin


class UserInteractor(CRUDInteractorMixin[User, UserCreate, UserUpdate, UserRead]):
    crud_repository = UserRepository
    enabled_delete = True

    async def create(self, schema: UserCreate) -> UserRead:
        existing_users = await self.crud_repository.filter(email=schema.email)
        if existing_users:
            raise UserAlreadyExistsError(schema.email)

        hashed_schema = UserCreateHashedPassword(
            email=schema.email,
            hashed_password=hash_password(schema.password),
        )
        return await self.crud_repository.create(hashed_schema)



