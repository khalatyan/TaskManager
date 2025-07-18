from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from task_manager.core.application.depends import get_user_interactor
from task_manager.core.application.interactor import UserInteractor
from task_manager.core.dependencies import get_current_user
from task_manager.core.exceptions import UserAlreadyExistsError
from task_manager.core.schemas import UserRead, UserCreate, UserUpdate, Token, UserAuth
from task_manager.core.utils import create_access_token
from task_manager.tasks.application.depends import get_task_repository, get_task_interactor
from task_manager.tasks.application.interactor import TaskInteractor
from task_manager.tasks.schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_create: TaskCreate,
        current_user: UserRead = Depends(get_current_user),
        interactor: TaskInteractor = Depends(get_task_interactor)
):
    task_create.created_by_id = current_user.id
    return await interactor.create(task_create)

@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    current_user: UserRead = Depends(get_current_user),
    interactor: TaskInteractor = Depends(get_task_interactor)
):
    return await interactor.filter(or_filters={"user_id": current_user.id, "created_by_id": current_user.id})

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    interactor: TaskInteractor = Depends(get_task_interactor)
):
    task = await interactor.get_by_id(task_id)
    if not task and not task.user_id == current_user.id and not task.created_by_id == current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
        task_id: int,
        task_update: TaskUpdate,
        current_user: UserRead = Depends(get_current_user),
        interactor: TaskInteractor = Depends(get_task_interactor)
):
    task = await interactor.get_by_id(task_id)
    if not task or not task.user_id == current_user.id and not task.created_by_id == current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return await interactor.update(task_id, task_update)