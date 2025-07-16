from task_manager.users.models import User
from task_manager.users.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead
from task_manager.utils.mixins.repository import CRUDRepositoryMixin


class UserRepository(CRUDRepositoryMixin[User, UserCreateHashedPassword, UserUpdate, UserRead]):
    model = User
    read_schema = UserRead
    enabled_delete = True
