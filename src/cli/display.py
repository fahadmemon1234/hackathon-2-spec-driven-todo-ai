"""
Display utilities for the Todo CLI app.
Formats task information for user-friendly display.
"""

from typing import List
from src.models.task import Task


def format_task_display(task: Task) -> str:
    """
    Format a single task for display with priority, tags, and status indicators.

    Args:
        task: The task to format

    Returns:
        Formatted string representation of the task
    """
    status = "[COMPLETED]" if task.completed else "[INCOMPLETE]"
    priority_indicator = get_priority_indicator(task.priority)
    tags_str = ", ".join(sorted(task.tags)) if task.tags else "None"

    return f"[{task.id}] {priority_indicator} {task.title} - {task.description} | Priority: {task.priority} | Tags: {tags_str} | Status: {status}"


def format_tasks_list(tasks: List[Task]) -> List[str]:
    """
    Format a list of tasks for display.
    
    Args:
        tasks: List of tasks to format
        
    Returns:
        List of formatted strings representing the tasks
    """
    return [format_task_display(task) for task in tasks]


def get_priority_indicator(priority: str) -> str:
    """
    Get a visual indicator for the priority level.

    Args:
        priority: Priority level ("High", "Medium", "Low")

    Returns:
        Visual indicator for the priority
    """
    if priority == "High":
        return "[HIGH]"
    elif priority == "Medium":
        return "[MED]"
    elif priority == "Low":
        return "[LOW]"
    else:
        return "[N/A]"  # Default for unknown priority levels


def format_task_brief(task: Task) -> str:
    """
    Format a brief representation of a task for compact display.

    Args:
        task: The task to format

    Returns:
        Brief formatted string representation of the task
    """
    status = "[C]" if task.completed else "[I]"
    priority_indicator = get_priority_indicator(task.priority)
    tags_count = len(task.tags)

    return f"[{task.id}] {priority_indicator} {status} {task.title} ({tags_count} tags)"