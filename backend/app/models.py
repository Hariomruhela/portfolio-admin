from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    image = Column(String)
    featured = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, )

    # updated 