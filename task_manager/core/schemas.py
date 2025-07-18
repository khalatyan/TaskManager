from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserAuth(UserBase):
    pass

class UserCreateHashedPassword(BaseModel):
    email: EmailStr
    hashed_password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class UserFullRead(UserRead):
    hashed_password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str