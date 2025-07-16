from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.database import get_session
from task_manager.users.crud import UserCRUD
from task_manager.users.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    crud = UserCRUD(session)
    user = await crud.create(user_create)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    crud = UserCRUD(session)
    user = await crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    crud = UserCRUD(session)
    user = await crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.update(user, user_update)
    return user