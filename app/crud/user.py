from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from app.core.auth import get_password_hash, verify_password


# Using passlib for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Retrieves user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Find user by Email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Retrieve list of users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Create new user, hashing password before storage
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email = user.email, hashed_password = hashed_password, is_superuser = user.is_superuser if hasattr(user, 'is_superuser') else False)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Authenticates user with email and password

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

