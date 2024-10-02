import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base, get_db
from app.core.security import UserRole

# Load environment variables
load_dotenv()

# Set the database to the test database
os.environ["DB_NAME"] = "edutrack_test"

# Construct the database URL
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SSLMODE = os.getenv("DB_SSLMODE")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

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

def test_create_user():
    response = client.post(
        "/api/v1/users/register",  # Updated endpoint
        json={"email": "test@example.com", "password": "testpassword", "role" : UserRole.STUDENT}
    )
    assert response.status_code == 200, f"Response: {response.json()}"
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["role"] == UserRole.STUDENT
    
def test_create_user_duplicate_email():
    response = client.post(
        "/api/v1/users/register",
        json = {"email": "test@example.com", "password": "testpassowrd", "role": UserRole.STUDENT}
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
    
def test_user_login():
    # First, create a user
    client.post(
        "/api/v1/users/register",
        json={"email": "login_test@example.com", "password": "testpassword", "role": UserRole.STUDENT}
    )
    
    # Now, try to login
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "login_test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
def test_read_users_me():
    # Create user and get token
    client.post(
        "/api/v1/users/register",
        json={"email": "me_test@example.com", "password": "testpassword", "role": UserRole.STUDENT}
    )
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "me_test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Use token to get user's data
    
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me_test@example.com"
    assert data["role"] == UserRole.STUDENT
    
def test_update_user_me():
     # First, create a user and get a token
    client.post(
        "/api/v1/users/register",
        json={"email": "update_test@example.com", "password": "testpassword", "role": UserRole.STUDENT}
    )
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "update_test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Now, use the token to update the user's own data
    response = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "updated_test@example.com", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated_test@example.com"

    # Verify that we can login with the new credentials
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "updated_test@example.com", "password": "newpassword"}
    )
    assert login_response.status_code == 200