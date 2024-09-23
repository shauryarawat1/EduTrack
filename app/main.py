from fastapi import FastAPI
from app.api import users
from app.db.base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")