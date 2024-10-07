from typing import Optional
from pydantic import BaseModel, EmailStr
from app.core.security import UserRole

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = UserRole.STUDENT
    
class UserCreate(UserBase):
    email: EmailStr
    password: str
    
class UserUpdate(UserBase):
    password: Optional[str] = None
    
class UserInDBBase(UserBase):
    id: Optional[int] = None
    
    class Config:
        from_attributes = True
        
class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str