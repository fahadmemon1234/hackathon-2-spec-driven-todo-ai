from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, and completion status.
    
    Attributes:
        id: Unique identifier assigned when task is created
        title: Title of the task (required, max 100 characters)
        description: Detailed description of the task (optional, max 500 characters)
        completed: Completion status (default: False)
    """
    id: int
    title: str
    description: str
    completed: bool = False

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