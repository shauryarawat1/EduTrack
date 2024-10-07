from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate

def get(db: Session, id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    return db.query(Course).offset(skip).limit(limit).all()

def create_with_instructor(db: Session, obj_in: CourseCreate, instructor_id: int) -> Course:
    db_obj = Course(**obj_in.dict(), instructor_id=instructor_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Course, obj_in: CourseUpdate) -> Course:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, id: int) -> Optional[Course]:
    obj = db.query(Course).get(id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def add_student(db: Session, db_obj: Course, student: User) -> Course:
    db_obj.students.append(student)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove_student(db: Session, db_obj: Course, student: User) -> Course:
    db_obj.students.remove(student)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_courses_by_instructor(db: Session, instructor_id: int) -> List[Course]:
    return db.query(Course).filter(Course.instructor_id == instructor_id).all()

def get_courses_by_student(db: Session, student_id: int) -> List[Course]:
    return db.query(Course).filter(Course.students.any(id=student_id)).all()