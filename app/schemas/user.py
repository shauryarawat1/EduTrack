from pydantic import BaseModel, EmailStr
from app.core.security import UserRole

# Fields common to all user schemas
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.STUDENT
    
# For creating new users
class UserCreate(UserBase):
    password: str
    
# For updating users
class UserUpdate(UserBase):
    password: str | None = None
    
# Represents the user as returned by API
class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        # Allows pydantic to work with SQLAlchemy models
        from_attributes = True