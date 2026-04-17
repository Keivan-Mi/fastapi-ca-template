# src/application/dtos/task_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...domain.value_objects.task_status import TaskStatus
from ...domain.value_objects.priority import Priority

@dataclass
class CreateTaskDTO:
    """DTO for creating a task - input from external layer"""
    title: str
    description: str
    priority: Priority
    due_date: Optional[datetime]
    user_id: int

@dataclass
class TaskFilterDTO:
    """DTO for filtering tasks"""
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_before: Optional[datetime] = None
    limit: int = 100
    offset: int = 0

@dataclass
class TaskResponseDTO:
    """DTO for returning task data - output to external layer"""
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
