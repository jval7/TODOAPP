import uuid
from datetime import datetime

import pydantic
from hashids import Hashids
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
hashids = Hashids(min_length=8)


class Task(BaseModel):
    id: str = pydantic.Field(default_factory=lambda: hashids.encode(int(uuid.uuid4().hex, 16)))
    title: str
    description: str = None
    completed: bool = False
    deadline: str
    complexity: str
    teacher: str
    classroom: str
    created_at: datetime = None
    updated_at: datetime = None


class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    completed = Column(Boolean, default=False)
    deadline = Column(String)
    complexity = Column(String)
    teacher = Column(String)
    classroom = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
