from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/edutrack"

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