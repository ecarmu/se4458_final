from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    is_company: bool = False

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_company: bool
    created_at: datetime

    class Config:
        from_attributes = True 