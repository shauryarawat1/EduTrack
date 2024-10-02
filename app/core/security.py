from enum import Enum
from fastapi import HTTPException, status

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