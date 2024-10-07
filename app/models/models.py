from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.security import UserRole

# Association table
user_course = Table('user_course', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)

    courses_teaching = relationship("Course", back_populates="instructor")
    courses_enrolled = relationship("Course", secondary=user_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    instructor_id = Column(Integer, ForeignKey("users.id"))

    instructor = relationship("User", back_populates="courses_teaching")
    students = relationship("User", secondary=user_course, back_populates="courses_enrolled")
    assignments = relationship("Assignment", back_populates="course")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="assignments")