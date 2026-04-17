# src/presentation/api/schemas/task_schema.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

from ....application.dtos.task_dto import TaskResponseDTO
from ....domain.value_objects.task_status import TaskStatus
from ....domain.value_objects.priority import Priority


class TaskCreateRequest(BaseModel):
    """Pydantic model for API request validation

    NOTE: This is PRESENTATION layer, NOT domain!
    Pydantic is framework-specific (FastAPI).
    We don't let it leak into Domain or Application layers.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    priority: Priority
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    """Response model"""
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None

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
            due_date=getattr(dto, "due_date", None),
        )
