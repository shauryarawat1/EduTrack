from sqlalchemy import Column, Integer, String, Boolean

from app.db.base import Base

class User(Base):
    # specifies name of table in database
    __tablename__ = "Users"
    
    # ID is the unique identifier
    id = Column(Integer, primary_key=True, index=True)
    
    # the email received from user
    email = Column(String, unique=True, index=True)
    
    # The password hashed from the original text
    hashed_password = Column(String)
    
    # Allows to deactivate users without deletion
    is_active = Column(Boolean, default=True)
    
    # Gives certain users more privileges
    is_superuser = Column(Boolean, default=False)