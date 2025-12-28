"""
Validation utilities for the Todo app.
"""

from typing import Set
from src.models.priority import VALID_PRIORITIES


def validate_priority(priority: str) -> bool:
    """
    Validate if the given priority is one of the valid priorities.
    
    Args:
        priority: Priority level to validate
        
    Returns:
        True if priority is valid, False otherwise
    """
    return priority in VALID_PRIORITIES


def validate_tags(tags: Set[str]) -> bool:
    """
    Validate if the given tags are valid (non-empty strings).
    
    Args:
        tags: Set of tags to validate
        
    Returns:
        True if tags are valid, False otherwise
    """
    if not isinstance(tags, set):
        return False

    for tag in tags:
        if not isinstance(tag, str) or not tag.strip():
            return False

    return True


def validate_task_id(task_id: int) -> bool:
    """
    Validate if the given task ID is valid (positive integer).
    
    Args:
        task_id: Task ID to validate
        
    Returns:
        True if task ID is valid, False otherwise
    """
    return isinstance(task_id, int) and task_id > 0


def validate_title(title: str) -> bool:
    """
    Validate if the given title is valid (1-100 characters).
    
    Args:
        title: Title to validate
        
    Returns:
        True if title is valid, False otherwise
    """
    return isinstance(title, str) and 1 <= len(title) <= 100


def validate_description(description: str) -> bool:
    """
    Validate if the given description is valid (0-500 characters).
    
    Args:
        description: Description to validate
        
    Returns:
        True if description is valid, False otherwise
    """
    return isinstance(description, str) and 0 <= len(description) <= 500