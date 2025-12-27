from typing import List, Optional
from src.models.task import Task


class TaskNotFoundError(Exception):
    """Exception raised when a task with a specified ID is not found."""
    pass


class TodoManager:
    """
    Business logic for todo operations.
    Manages a collection of Task objects in memory.
    """
    
    def __init__(self):
        """Initialize the TodoManager with an empty list of tasks and next ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1
    
    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task with the given title and description.
        
        Args:
            title: The title of the task (1-100 characters)
            description: The description of the task (0-500 characters)
            
        Returns:
            The ID of the newly created task
            
        Raises:
            ValueError: If title or description don't meet validation requirements
        """
        # Validate inputs according to data-model.md
        if not (1 <= len(title) <= 100):
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(title)}")
        
        if description and not (1 <= len(description) <= 500):
            raise ValueError(f"Description must be between 1 and 500 characters, got {len(description)}")
        
        # Create new task with unique ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        
        # Add to tasks list and increment ID counter
        self._tasks.append(task)
        task_id = self._next_id
        self._next_id += 1
        
        return task_id
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the system.
        
        Returns:
            A list of all Task objects
        """
        return self._tasks.copy()  # Return a copy to prevent external modification
    
    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a specific task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object with the specified ID
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} does not exist.")
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update the title and/or description of a task by its ID.
        
        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            
        Returns:
            True if the task was successfully updated, False otherwise
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
            ValueError: If new title or description don't meet validation requirements
        """
        task = self.get_task_by_id(task_id)
        
        # Use existing values if new values are not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description
        
        # Validate inputs according to data-model.md
        if not (1 <= len(new_title) <= 100):
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(new_title)}")
        
        if new_description and not (1 <= len(new_description) <= 500):
            raise ValueError(f"Description must be between 1 and 500 characters, got {len(new_description)}")
        
        # Update the task
        task.title = new_title
        task.description = new_description
        
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was successfully deleted, False otherwise
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        self._tasks.remove(task)
        return True
    
    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by its ID.
        
        Args:
            task_id: The ID of the task to mark as complete
            
        Returns:
            True if the task was successfully marked as complete, False otherwise
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        task.completed = True
        return True
    
    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by its ID.
        
        Args:
            task_id: The ID of the task to mark as incomplete
            
        Returns:
            True if the task was successfully marked as incomplete, False otherwise
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        task.completed = False
        return True