from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

user_course = Table(
    'user_course', Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("course_id", Integer, ForeignKey("course.id"))
)

class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    instructor_id = Column(Integer, ForeignKey("user.id"))
    
    instructor = relationship("User", back_populates="courses_teaching")
    students = relationship("User", secondary=user_course, back_populates="courses_enrolled")
    assignments = relationship("Assignment", back_populates="course")