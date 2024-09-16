from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import User, UserCreate
from app.db.base import get_db

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