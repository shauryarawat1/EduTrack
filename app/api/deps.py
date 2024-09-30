from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud import user as user_crud
from app.db.base import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    '''Credentials error if not verified'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {'WWW-Authenticate': "Bearer"},
    )
    
    try:
        # Decodes the jwt token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Retrieves the email
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # If email is verified then gets user
    user = user_crud.get_user_by_email(db, email = email)
    
    # Returns error if not verified
    if user is None:
        raise credentials_exception
    
    return user