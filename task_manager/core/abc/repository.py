from task_manager.core.models import User
from task_manager.core.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead
from task_manager.utils.mixins.repository import CRUDRepositoryMixin
from task_manager.utils.mixins_abc.repositories import AbstractCRUDRepository


class AbstractUserRepository(AbstractCRUDRepository[User, UserCreateHashedPassword, UserUpdate, UserRead]):
    """
    Абстрактный базовый класс для CRUD-репозитория пользователя.
    """

