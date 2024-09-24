from pydantic import BaseModel
from typing import List, Optional

# Defines basic attributes of course
class CourseBase(Optional):
    title: str
    description: Optional[str] = None
    
# Used for creating new courses
class CourseCreate(CourseBase):
    pass

# Contains basic information returned by API
class Course(CourseBase):
    id: int
    instructor_id: int
    
    class Config:
        from_attributes = True
        
# List of student IDs
class CourseWithStudents(Course):
    students: List[int] = []
    
# Full course data as stored in DB
class CourseInDB(Course):
    students: List[int] = []
    assignments: List[int] = []