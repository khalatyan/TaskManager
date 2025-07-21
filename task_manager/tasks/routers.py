from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from task_manager.core.dependencies import get_current_user
from task_manager.core.schemas import UserRead
from task_manager.tasks.application.controller import TaskController
from task_manager.tasks.application.depends import get_task_controller
from task_manager.tasks.schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_create: TaskCreate,
        current_user: UserRead = Depends(get_current_user),
        controller: TaskController = Depends(get_task_controller)
):
    task_create.created_by_id = current_user.id
    return await controller.create(task_create)

@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    current_user: UserRead = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    return await controller.filter(filters={"or": [{"user_id": current_user.id}, {"created_by_id": current_user.id}]})

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    return await controller.get_by_id(task_id, current_user)

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    return await controller.update(task_id, task_update, current_user)