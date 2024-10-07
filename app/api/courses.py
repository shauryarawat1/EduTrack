from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import course as course_crud
from app.schemas.course import CourseCreate, Course, CourseUpdate
from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.models import User, Course
from app.core.security import UserRole, check_user_role

router = APIRouter()
