from task_manager.tasks.abc.repository import AbstractTaskRepository
from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskCreate, TaskUpdate, TaskRead
from task_manager.utils.mixins.repository import CRUDRepositoryMixin


class TaskRepository(AbstractTaskRepository, CRUDRepositoryMixin[Task, TaskCreate, TaskUpdate, TaskRead]):
    model = Task
    read_schema = TaskRead
