from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

from task_manager.settings import SECRET_KEY, ALGORITHM
from task_manager.core.application.depends import get_user_repository
from task_manager.core.application.repository import UserRepository
from task_manager.core.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), repo: UserRepository = Depends(get_user_repository)) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = await repo.filter(and_filters={"email": username})
    if user is None:
        raise credentials_exception

    return user[0]
