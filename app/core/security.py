from enum import Enum
from fastapi import HTTPException, status
from passlib.context import CryptContext

# Represents different roles in system
class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    
# Checks if user's role is in allowed roles
def check_user_role(user, allowed_roles):
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "User does not have enough privileges"
        )
        
# Password hashing

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

# Verify password

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

