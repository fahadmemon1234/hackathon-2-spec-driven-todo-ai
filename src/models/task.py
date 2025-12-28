from dataclasses import dataclass
from typing import Optional, Set


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, completion status, priority, and tags.

    Attributes:
        id: Unique identifier assigned when task is created
        title: Title of the task (required, max 100 characters)
        description: Detailed description of the task (optional, max 500 characters)
        completed: Completion status (default: False)
        priority: Priority level of the task (default: "Medium")
        tags: Set of tags associated with the task (default: empty set)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"
    tags: Set[str] = None

    def __post_init__(self):
        """Validate the task attributes after initialization."""
        if not (1 <= len(self.title) <= 100):
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(self.title)}")

        if self.description and not (1 <= len(self.description) <= 500):
            raise ValueError(f"Description must be between 1 and 500 characters, got {len(self.description) if self.description else 0}")

        if not isinstance(self.completed, bool):
            raise ValueError(f"Completed status must be a boolean value, got {type(self.completed)}")

        if self.id <= 0:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        # Initialize tags as an empty set if None was passed
        if self.tags is None:
            self.tags = set()

        # Validate priority
        valid_priorities = {"High", "Medium", "Low"}
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}, got {self.priority}")

        # Validate tags
        if not isinstance(self.tags, set):
            raise ValueError(f"Tags must be a set, got {type(self.tags)}")

        for tag in self.tags:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError(f"Tags must be non-empty strings, got {tag}")