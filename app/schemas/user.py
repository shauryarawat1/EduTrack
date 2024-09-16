from pydantic import BaseModel, EmailStr

# Fields common to all user schemas
class UserBase(BaseModel):
    email: EmailStr
    
# For creating new users
class UserCreate(UserBase):
    password: str
    
# Represents the user as returned by API
class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        # Allows pydantic to work with SQLAlchemy models
        orm_mode = True