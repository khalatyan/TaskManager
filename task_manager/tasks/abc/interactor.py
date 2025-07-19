from fastapi import Depends

from task_manager.tasks.application.repository import TaskRepository
from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskUpdate, TaskCreate, TaskRead
from task_manager.core.application.repository import UserRepository
from task_manager.core.exceptions import UserAlreadyExistsError
from task_manager.core.models import User
from task_manager.core.schemas import UserCreate, UserUpdate, UserCreateHashedPassword, UserRead, UserAuth, \
    UserFullRead
from task_manager.core.utils import hash_password, verify_password
from task_manager.utils.mixins.interactors import CRUDInteractorMixin
from task_manager.utils.mixins_abc.interactors import AbstractCRUDInteractor


class AbstractTaskInteractor(AbstractCRUDInteractor[Task, TaskCreate, TaskUpdate, TaskRead]):
    """
    Абстрактный интерфейс для бизнес-логики CRUD-операций задач.
    """
