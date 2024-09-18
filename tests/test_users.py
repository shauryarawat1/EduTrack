from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db

# Using SQLLite for testing as it doesnt require a server
SQLALCHEMY_DATABASE_URL = "sqllite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_name_thread":False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override get_db to use test database