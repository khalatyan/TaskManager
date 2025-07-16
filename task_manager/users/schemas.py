from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
