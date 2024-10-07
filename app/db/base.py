from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Base factory to create database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Dependency to be used in FastAPI routes to get database session
def get_db():
    db = SessionLocal()
    try:
        # Ensures that database session is yielded for use in routes
        yield db
    finally:
        # Ensures that database session is closed after each request
        db.close()

# Importing all the models from the folder (User, Course, etc)
from app.models.user import User
from app.models.course import Course
from app.models.association import user_course

# Create tables
Base.metadata.create_all(bind=engine)
