from typing import Optional, List

from pydantic import BaseModel

class CourseBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CourseCreate(CourseBase):
    title: str

class CourseUpdate(CourseBase):
    pass

class CourseInDBBase(CourseBase):
    id: int
    instructor_id: int

    class Config:
        from_attributes = True

class Course(CourseInDBBase):
    students: List[int] = []

class CourseInDB(CourseInDBBase):
    pass