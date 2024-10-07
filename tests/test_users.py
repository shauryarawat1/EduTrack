import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base_class import Base
from app.db.base import get_db
from app.core.config import settings
from app.models.user import User
from app.models.course import Course
from app.core.security import UserRole

# Load environment variables
load_dotenv()

# Set the database to the test database
os.environ["DB_NAME_TEST"] = "edutrack_test"

# Use the SQLALCHEMY_DATABASE_URI from settings
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a TestingSessionLocal class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ... rest of the test functions remain the same ...