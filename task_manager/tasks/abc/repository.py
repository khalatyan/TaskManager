from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskCreate, TaskUpdate, TaskRead
from task_manager.utils.mixins.repository import CRUDRepositoryMixin
from task_manager.utils.mixins_abc.repositories import AbstractCRUDRepository


class AbstractTaskRepository(AbstractCRUDRepository[Task, TaskCreate, TaskUpdate, TaskRead]):
    """
    Абстрактный базовый класс для CRUD-репозитория задач.
    """
