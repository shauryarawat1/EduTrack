from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate
from typing import List, Optional

def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    return db.query(Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: CourseCreate, instructor_id: int) -> Course:
    db_course = Course(**course.dict(), instructor_id = instructor_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Optional[Course]:
    db_course = get_course(db, course_id)
    
    if db_course:
        update_data = course_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_course, key, value)
            
        db.commit()
        db.refresh(db_course)
        
    return db_course

def delete_course(db: Session, course_id: int) -> bool:
    db_course = get_course(db, course_id)
    
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    
    return False

def enroll_student(db: Session, course_id: int, student_id: int) -> Optional[Course]:
    course = get_course(db, course_id)
    
    student = db.query(User).filter(User.id == student_id).first()
    
    if course and student:
        course.students.append(student)
        db.commit()
        db.refresh(course)
        
    return course