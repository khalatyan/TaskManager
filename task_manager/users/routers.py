from fastapi import APIRouter, HTTPException, status, Depends

from task_manager.users.application.depends import get_user_interactor
from task_manager.users.application.interactor import UserInteractor
from task_manager.users.exceptions import UserAlreadyExistsError
from task_manager.users.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, interactor: UserInteractor = Depends(get_user_interactor)):
    try:
        user = await interactor.create(user_create)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, interactor: UserInteractor = Depends(get_user_interactor)):
    user = await interactor.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, interactor: UserInteractor = Depends(get_user_interactor)):
    user = await interactor.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await interactor.update(user_id, user_update)
    return user