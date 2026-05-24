# src/domain/services/task_hierarchy.py
"""
DAG / forest helpers: parent_id defines hierarchy; prevent cycles on reparent.
"""

from __future__ import annotations

from ..entities.task import Task
from ..exceptions import InvalidParentException


def build_children_index(tasks: list[Task]) -> dict[int, list[int]]:
    """parent_id -> [child task ids]"""
    index: dict[int, list[int]] = {}
    for task in tasks:
        if task.parent_id is not None:
            index.setdefault(task.parent_id, []).append(task.id)
    return index


def collect_descendant_ids(
        task_id: int,
        children_index: dict[int, list[int]],
) -> set[int]:
    """All descendant ids (child, grandchild, ...) via BFS."""
    descendants: set[int] = set()
    queue = list(children_index.get(task_id, []))
    while queue:
        child_id = queue.pop(0)
        if child_id in descendants:
            continue
        descendants.add(child_id)
        queue.extend(children_index.get(child_id, []))
    return descendants


def validate_reparent(
        task: Task,
        new_parent_id: int | None,
        children_index: dict[int, list[int]],
) -> None:
    """
    Only rule: new parent must not be this task or any of its descendants (no loops).
    """
    if new_parent_id is None:
        return

    if new_parent_id == task.id:
        raise InvalidParentException("A task cannot be its own parent")

    if new_parent_id in collect_descendant_ids(task.id, children_index):
        raise InvalidParentException(
            "Cannot assign a descendant as parent; that would create a cycle"
        )
