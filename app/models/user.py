from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.core.security import UserRole

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    
    courses_teaching = relationship("Course", back_populates="instructor")
    courses_enrolled = relationship("Course", secondary="user_course", back_populates="students")
