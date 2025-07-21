from abc import ABC

from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskUpdate, TaskCreate, TaskRead
from task_manager.utils.mixins_abc.interactors import AbstractCRUDInteractor


class AbstractTaskInteractor(AbstractCRUDInteractor[Task, TaskCreate, TaskUpdate, TaskRead], ABC):
    """
    Абстрактный интерфейс для бизнес-логики CRUD-операций задач.
    """
