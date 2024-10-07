from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.api import deps
from app.core.security import UserRole

router = APIRouter()

@router.post("/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.course.create_with_instructor(db=db, obj_in=course, instructor_id=current_user.id)

@router.get("/", response_model=List[schemas.Course])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    courses = crud.course.get_multi(db, skip=skip, limit=limit)
    return courses

@router.get("/{course_id}", response_model=schemas.Course)
def read_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN] or (current_user.role == UserRole.INSTRUCTOR and course.instructor_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    course = crud.course.update(db, db_obj=course, obj_in=course_update)
    return course

@router.delete("/{course_id}", response_model=schemas.Course)
def delete_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != UserRole.ADMIN and (current_user.role != UserRole.INSTRUCTOR or course.instructor_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    course = crud.course.remove(db, id=course_id)
    return course

@router.post("/{course_id}/enroll", response_model=schemas.Course)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user in course.students:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")
    course = crud.course.add_student(db, db_obj=course, student=current_user)
    return course