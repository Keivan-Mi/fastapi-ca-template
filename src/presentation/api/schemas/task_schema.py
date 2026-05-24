# src/presentation/api/schemas/task_schema.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

from ....application.dtos.task_dto import TaskResponseDTO
from ....domain.value_objects.task_status import TaskStatus
from ....domain.value_objects.priority import Priority


class TaskCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    priority: Priority
    due_date: Optional[datetime] = None
    parent_id: Optional[int] = None
    estimated_time: Optional[int] = Field(None, ge=0)


class TaskUpdateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    parent_id: Optional[int] = None
    estimated_time: Optional[int] = Field(None, ge=0)


class TaskResponse(BaseModel):
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

    @classmethod
    def from_dto(cls, dto: TaskResponseDTO) -> "TaskResponse":
        return cls(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            status=dto.status,
            priority=dto.priority,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            due_date=dto.due_date,
            estimated_time=dto.estimated_time,
            parent_id=dto.parent_id,
        )
