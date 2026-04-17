# src/presentation/api/task_controller.py
from typing import Optional, List

from fastapi import APIRouter, Depends, status

from ...config.dependencies import (
    get_create_task_use_case,
    get_get_tasks_use_case,
    get_current_user,
)
from ...application.use_cases.create_task import CreateTaskUseCase
from ...application.use_cases.get_tasks import GetTasksUseCase
from ...application.dtos.task_dto import CreateTaskDTO, TaskFilterDTO
from .schemas.task_schema import TaskCreateRequest, TaskResponse
from ...domain.value_objects.priority import Priority
from ...domain.value_objects.task_status import TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    request: TaskCreateRequest,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
    current_user_id: int = Depends(get_current_user),
) -> TaskResponse:
    """Create a new task for the current user."""
    dto = CreateTaskDTO(
        title=request.title,
        description=request.description,
        priority=request.priority,
        due_date=request.due_date,
        user_id=current_user_id,
    )
    result = await use_case.execute(dto)
    return TaskResponse.from_dto(result)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    limit: int = 100,
    offset: int = 0,
    use_case: GetTasksUseCase = Depends(get_get_tasks_use_case),
    current_user_id: int = Depends(get_current_user),
) -> List[TaskResponse]:
    """List tasks for the current user with optional filters."""
    filters = TaskFilterDTO(status=status, priority=priority, limit=limit, offset=offset)
    dtos = await use_case.execute(user_id=current_user_id, filters=filters)
    return [TaskResponse.from_dto(d) for d in dtos]
