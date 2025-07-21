from abc import ABC, abstractmethod

from task_manager.core.schemas import UserRead
from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskUpdate, TaskCreate, TaskRead
from task_manager.utils.mixins_abc.controllers import AbstractCRUDController


class AbstractTaskController(AbstractCRUDController[Task, TaskCreate, TaskUpdate, TaskRead], ABC):
    """
    Абстрактный интерфейс для контроллера CRUD-операций задач.
    """

    @abstractmethod
    async def update(self, task_id: int, schema: TaskUpdate, current_user: UserRead) -> TaskRead:
        """
        Обновление задачи
        :param task_id: Идентификатор объекта, который нужно обновить.
        :param schema: Схема с данными для обновления (update schema).
        :param current_user: Схема с данными с пользователем.
        :return: Обновлённый объект.
        """
        ...

    @abstractmethod
    async def get_by_id(self, task_id: int, current_user: UserRead) -> TaskRead:
        """
        Получить объект по его ID.
        :param task_id: Идентификатор объекта, который нужно обновить.
        :param current_user: Схема с данными с пользователем.
        :return: Обновлённый объект.
        """
        ...