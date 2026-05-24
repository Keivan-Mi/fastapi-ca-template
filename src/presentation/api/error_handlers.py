# src/presentation/api/error_handlers.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from ...domain.exceptions import (
    TaskNotFoundException,
    UnauthorizedAccessException,
    InvalidParentException,
)
from ...application.exceptions import ValidationException


def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found", "task_id": exc.task_id}
        )

    @app.exception_handler(UnauthorizedAccessException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedAccessException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "Unauthorized access"}
        )

    @app.exception_handler(InvalidParentException)
    async def invalid_parent_handler(request: Request, exc: InvalidParentException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(exc)},
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Validation failed", "details": exc.details}
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"}
        )
