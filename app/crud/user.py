from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

# Using passlib for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Retrieves user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Find user by Email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Retrieve list of users
def get_users(db: Session, skip: int = 0, limit: int = 100)