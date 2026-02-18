from typing import Optional
from pydantic import ConfigDict, BaseModel, EmailStr
from uuid import UUID, uuid4


class UserBase(BaseModel):
    email: EmailStr 
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBase(UserBase):
    id: UUID
    hashed_password: str


class User(UserBase):
    id: UUID
