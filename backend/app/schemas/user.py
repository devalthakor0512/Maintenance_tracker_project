from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
