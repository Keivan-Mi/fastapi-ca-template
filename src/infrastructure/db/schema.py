# src/infrastructure/db/schema.py
"""Recreate tables when SQLite schema no longer matches ORM models."""

from sqlalchemy import inspect

from .models import Base

# Columns removed from the model — if still in DB, reset tables
_OBSOLETE_COLUMNS = frozenset({"group_name", "level"})
_REQUIRED_COLUMNS = frozenset({
    "id", "title", "description", "status", "priority",
    "created_at", "updated_at", "user_id", "due_date",
    "estimated_time", "parent_id",
})


def _needs_reset(connection) -> bool:
    inspector = inspect(connection)
    if not inspector.has_table("tasks"):
        return False
    names = {c["name"] for c in inspector.get_columns("tasks")}
    if names & _OBSOLETE_COLUMNS:
        return True
    if not _REQUIRED_COLUMNS.issubset(names):
        return True
    return False


def sync_database_schema(connection) -> None:
    if _needs_reset(connection):
        Base.metadata.drop_all(connection)
    Base.metadata.create_all(connection)
