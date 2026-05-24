# src/domain/exceptions.py

class DomainException(Exception):
    pass

class TaskNotFoundException(DomainException):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")

class UnauthorizedAccessException(DomainException):
    def __init__(self, user_id: int, resource_id: int):
        self.user_id = user_id
        self.resource_id = resource_id
        super().__init__(
            f"User {user_id} is not authorized to access resource {resource_id}"
        )

class InvalidTaskStateException(DomainException):
    pass


class InvalidParentException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
