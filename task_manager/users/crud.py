from task_manager.users.models import User
from task_manager.users.schemas import UserCreate, UserUpdate
from task_manager.utils.mixins.crud import CRUDMixin


class UserCRUD(CRUDMixin[User, UserCreate, UserUpdate]):
    model = User
    enabled_delete = True
