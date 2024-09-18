from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db
import os

os.environ["DB_NAME"] = "edutrack_test"

# Using SQLLite for testing as it doesnt require a server
SQLALCHEMY_DATABASE_URL = "sqllite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_name_thread":False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override get_db to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
        
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test creates a user and retrieves it
def test_create_user():
    response = client.post(
        "/api/v1/users",
        json={"email":"test@example.com", "password":"testpassword"}
    )
    
    assert response.status_code == 200, response.text
    data = response.json()
    
    assert data["email"] == "test@example.com"
    assert "id" in data
    user_id = data["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == user_id