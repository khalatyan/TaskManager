from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from task_manager.users.application.depends import get_user_interactor
from task_manager.users.application.interactor import UserInteractor
from task_manager.users.dependencies import get_current_user
from task_manager.users.exceptions import UserAlreadyExistsError
from task_manager.users.schemas import UserRead, UserCreate, UserUpdate, Token, UserAuth
from task_manager.users.utils import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, interactor: UserInteractor = Depends(get_user_interactor)):
    try:
        user = await interactor.create(user_create)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), interactor: UserInteractor = Depends(get_user_interactor)):
    user_schema = UserAuth(
        email=form_data.username,
        password=form_data.password
    )
    user = await interactor.authenticate_user(user_schema)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: UserRead = Depends(get_current_user),
    interactor: UserInteractor = Depends(get_user_interactor)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="User not found")
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