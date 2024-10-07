from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import course as course_crud
from app.schemas.course import CourseCreate, Course, CourseUpdate
from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.models import User, Course
from app.core.security import UserRole, check_user_role

router = APIRouter()

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_user_role(current_user, [UserRole.INSTRUCTOR, UserRole.ADMIN])
    return course_crud.create_course(db=db, course=course, instructor_id=current_user.id)

@router.get("/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_course = course_crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    courses = course_crud.get_courses(db, skip=skip, limit=limit)
    return courses

@router.put("/{course_id}", response_model=Course)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_course = course_crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != UserRole.ADMIN and db_course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return course_crud.update_course(db, course_id=course_id, course_update=course_update)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_course = course_crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != UserRole.ADMIN and db_course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    course_crud.delete_course(db, course_id=course_id)

@router.post("/{course_id}/enroll/{student_id}", response_model=Course)
def enroll_student_in_course(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_user_role(current_user, [UserRole.INSTRUCTOR, UserRole.ADMIN])
    db_course = course_crud.enroll_student(db, course_id=course_id, student_id=student_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course or student not found")
    return db_course