from fastapi import Depends, HTTPException

from task_manager.core.schemas import UserRead
from task_manager.tasks.abc.controller import AbstractTaskController
from task_manager.tasks.application.interactor import TaskInteractor
from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskUpdate, TaskCreate, TaskRead
from task_manager.utils.mixins.controllers import CRUDControllerMixin


class TaskController(AbstractTaskController, CRUDControllerMixin[Task, TaskCreate, TaskUpdate, TaskRead]):
    crud_interactor = TaskInteractor

    def __init__(
        self,
        crud_interactor: TaskInteractor = Depends(TaskInteractor),
    ):
        super().__init__(crud_interactor)

    async def update(self, task_id: int, schema: TaskUpdate, current_user: UserRead) -> TaskRead:
        task = await self.crud_interactor.get_by_id(task_id)
        if not task or not task.user_id == current_user.id and not task.created_by_id == current_user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        return await self.crud_interactor.update(task_id, schema)

    async def get_by_id(self, task_id: int, current_user: UserRead) -> TaskRead:
        task = await self.crud_interactor.get_by_id(task_id)
        if not task or not task.user_id == current_user.id and not task.created_by_id == current_user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

