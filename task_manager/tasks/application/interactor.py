from fastapi import Depends

from task_manager.tasks.application.repository import TaskRepository
from task_manager.tasks.abc.interactor import AbstractTaskInteractor
from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskUpdate, TaskCreate, TaskRead

from task_manager.utils.mixins.interactors import CRUDInteractorMixin


class TaskInteractor(AbstractTaskInteractor, CRUDInteractorMixin[Task, TaskCreate, TaskUpdate, TaskRead]):
    crud_repository = TaskRepository

    def __init__(
        self,
        crud_repository: TaskRepository = Depends(TaskRepository)
    ):
        super().__init__(crud_repository)

