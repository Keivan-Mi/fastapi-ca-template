# src/infrastructure/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ...domain.value_objects.task_status import TaskStatus
from ...domain.value_objects.priority import Priority

Base = declarative_base()


class UserModel(Base):
    """Minimal user model for FK. In a full app this would live in a user module."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)


class TaskModel(Base):
    """SQLAlchemy ORM model - Infrastructure concern

    IMPORTANT: This is NOT our domain entity!
    Keep domain pure. Use mappers to convert between ORM and domain.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(SQLEnum(Priority), nullable=False, default=Priority.MEDIUM)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(DateTime, nullable=True)
