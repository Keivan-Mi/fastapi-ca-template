# src/application/dtos/task_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...domain.value_objects.task_status import TaskStatus
from ...domain.value_objects.priority import Priority

@dataclass
class CreateTaskDTO:
    title: str
    description: str
    priority: Priority
    due_date: Optional[datetime]
    user_id: int
    parent_id: Optional[int] = None
    estimated_time: Optional[int] = None


@dataclass
class UpdateTaskDTO:
    task_id: int
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    parent_id: Optional[int] = None
    estimated_time: Optional[int] = None
    update_parent: bool = False

@dataclass
class TaskFilterDTO:
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_before: Optional[datetime] = None
    limit: int = 100
    offset: int = 0

@dataclass
class TaskResponseDTO:
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    estimated_time: Optional[int] = None
    parent_id: Optional[int] = None
