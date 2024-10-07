from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import users, courses

from app.core.config import settings

app = FastAPI(title = settings.PROJECT_NAME, openapi_url = f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled functions

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )
    
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])

@app.get("/")
def root():
    return {"message": "Welcome to EduTrack API"}