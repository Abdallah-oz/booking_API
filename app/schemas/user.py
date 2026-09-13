from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict


class UserRole(str, Enum):
    CLIENT = "client"
    HOTEL = "hotel"



class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    role: str  
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)