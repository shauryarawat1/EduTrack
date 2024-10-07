from sqlalchemy.orm import declarative_base

Base = declarative_base()

# This function will be used to import all models
def import_models():
    from app.models.user import User
    from app.models.course import Course
    from app.models.assignment import Assignment
    return User, Course, Assignment
