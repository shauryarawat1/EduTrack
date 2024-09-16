from fastapi import FastAPI
from app.api import users
from app.db.base import Base, engine

# Creates database tables
Base.metadata.create_all(bind=engine)

# Creates FastAPI Instance
app = FastAPI(title="EduTrack")

# Adds user routes to app
app.include_router(users.router, prefix="/api/v1")

@app.get("/")

async def root():
    return {"message": "Welcome to EduTrack API"}