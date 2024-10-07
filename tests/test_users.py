import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.core.config import settings
from app.models.user import User
from app.core.security import UserRole

# Test database setup
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={"email": "test@example.com", "password": "testpassword", "role": UserRole.STUDENT.value}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["role"] == UserRole.STUDENT.value

def test_create_user_duplicate_email():
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={"email": "test@example.com", "password": "testpassword", "role": UserRole.STUDENT.value}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

# ... (rest of the tests would need similar adjustments)