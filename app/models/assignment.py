from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Assignment(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    course_id = Column(Integer, ForeignKey("course.id"))

    course = relationship("Course", back_populates="assignments")