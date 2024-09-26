from fastapi import FastAPI
from app.api import courses, users, auth
from app.db.base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduTrack")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(auth.router, prefix = "/api/v1/auth", tags=["auth"])

@app.get("/")

def read_root():
    return {"message": ""}