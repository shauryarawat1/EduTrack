from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserUpdate
from app.models.models import User
from app.db.base import get_db
from app.api.deps import get_current_user
from app.core.security import UserRole, check_user_role

# Router to group related routes
router = APIRouter()

@router.post("/users/", response_model=User)

# Depends injects a database session into each route
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_crud.create_user(db=db, user=user)

@router.get("/users/", response_model= list[User])

def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip = skip, limit = limit)
    return users

@router.get("/users/{user_id}", response_model=User)

def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id = user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

# Allows authenticated users to get their own information 
@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_crud.update_user(db, user_id=current_user.id, user=user_update)
