from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud import course as course_crud
from app.schemas.course import CourseCreate, Course, CourseUpdate
from app.db.base import get_db

router = APIRouter()

# Creates a new course

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)

def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    return course_crud.create_course(db = db, course = course, instructor_id=1)

# Retrieves a specific course

@router.get("/{course_id}", response_model=Course)

def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course_crud.get_course(db, course_id=course_id)
    
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return db_course

@router.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = course_crud.get_courses(db, skip=skip, limit=limit)
    return courses