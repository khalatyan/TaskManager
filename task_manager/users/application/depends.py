from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.database import get_session
from task_manager.users.application.interactor import UserInteractor
from task_manager.users.application.repository import UserRepository


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_user_interactor(
    repo: UserRepository = Depends(get_user_repository)
) -> UserInteractor:
    return UserInteractor(repo)