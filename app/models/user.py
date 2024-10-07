from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.course import user_course
from app.db.base import Base
from app.core.security import UserRole
from app.models.association import user_course

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
    
    # Gives student role by default to the user
    role = Column(Enum(UserRole), default = UserRole.STUDENT)
    
    # Relationships with the course model
    courses_teaching = relationship("Course", back_populates="instructor")
    courses_enrolled = relationship("Course", secondary=user_course, back_populates="students")
    
    def __repr__(self):
        return f"<User(id = {self.id}, email = '{self.email}', is_active = {self.is_active})>"