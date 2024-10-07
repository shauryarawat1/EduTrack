from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

user_course = Table('user_course', Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("course_id", Integer, ForeignKey()))