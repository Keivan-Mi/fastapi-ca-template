# src/application/exceptions.py
"""Application-layer exceptions (use case validation, etc.)."""


class ApplicationException(Exception):
    """Base exception for application layer."""
    pass


class ValidationException(ApplicationException):
    """Raised when use case input validation fails."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}
