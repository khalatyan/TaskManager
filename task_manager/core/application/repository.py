from task_manager.core.models import User
from task_manager.core.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead
from task_manager.utils.mixins.repository import CRUDRepositoryMixin


class UserRepository(CRUDRepositoryMixin[User, UserCreateHashedPassword, UserUpdate, UserRead]):
    model = User
    read_schema = UserRead
    enabled_delete = True
