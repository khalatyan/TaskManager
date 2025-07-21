from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.database import get_session
from task_manager.tasks.application.controller import TaskController
from task_manager.tasks.application.interactor import TaskInteractor
from task_manager.tasks.application.repository import TaskRepository
from task_manager.core.application.interactor import UserInteractor
from task_manager.core.application.repository import UserRepository


def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)

def get_task_interactor(
    repo: TaskRepository = Depends(get_task_repository)
) -> TaskInteractor:
    return TaskInteractor(repo)

def get_task_controller(
    interactor: TaskInteractor = Depends(get_task_interactor)
) -> TaskController:
    return TaskController(interactor)