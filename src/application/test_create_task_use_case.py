# tests/application/test_create_task_use_case.py
from datetime import datetime

import pytest
from unittest.mock import AsyncMock
from src.application.use_cases.create_task import CreateTaskUseCase
from src.application.dtos.task_dto import CreateTaskDTO
from src.domain.entities.task import Task
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.task_status import TaskStatus


@pytest.mark.asyncio
async def test_create_task_success():
    """Test use case WITHOUT database, web server, or external dependencies!
    """
    # Mock repository (fake implementation)
    mock_repo = AsyncMock()
    mock_repo.create.return_value = Task(
        id=1, title="Test", description="Test task",
        status=TaskStatus.TODO, priority=Priority.HIGH,
        created_at=datetime.now(), updated_at=datetime.now(),
        user_id=1, due_date=None
    )

    # Create use case with mock
    use_case = CreateTaskUseCase(task_repository=mock_repo)

    # Execute
    dto = CreateTaskDTO(
        title="Test", description="Test task",
        priority=Priority.HIGH, due_date=None, user_id=1
    )
    result = await use_case.execute(dto)

    # Assert
    assert result.id == 1
    assert result.title == "Test"
    mock_repo.create.assert_called_once()
