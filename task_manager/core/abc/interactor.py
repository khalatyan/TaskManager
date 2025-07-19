from fastapi import Depends

from task_manager.core.application.repository import UserRepository
from task_manager.core.exceptions import UserAlreadyExistsError
from task_manager.core.models import User
from task_manager.core.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead, UserAuth, \
    UserFullRead
from task_manager.core.utils import hash_password, verify_password
from task_manager.utils.mixins.interactors import CRUDInteractorMixin
from task_manager.utils.mixins_abc.interactors import AbstractCRUDInteractor


class AbstractUserInteractor(AbstractCRUDInteractor[User, UserCreate, UserUpdate, UserRead]):
    """
    Абстрактный интерфейс для бизнес-логики CRUD-операций пользователя.
    """

    async def authenticate_user(self, user: UserAuth) -> UserRead | None:
        """
        Аутентификация пользователя

        :param user: Данные аутентификации пользователя.
        :return: Аутентифицироанного пользователи или None.
        """
        ...



