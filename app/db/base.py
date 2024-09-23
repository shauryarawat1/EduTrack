from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SSLMODE = os.getenv("DB_SSLMODE")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

# Manage connections to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Base factory to create database connections
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

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

# Create tables 
Base.metadata.create_all(bind=engine)