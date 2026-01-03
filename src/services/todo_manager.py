from typing import List, Optional, Set
from src.models.task import Task
from src.models.priority import VALID_PRIORITIES


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

    def add_task(self, title: str, description: str = "", priority: str = "Medium", tags: Set[str] = None) -> int:
        """
        Add a new task with the given title, description, priority, and tags.

        Args:
            title: The title of the task (1-100 characters)
            description: The description of the task (0-500 characters)
            priority: The priority level of the task (default: "Medium")
            tags: A set of tags for the task (default: empty set)

        Returns:
            The ID of the newly created task

        Raises:
            ValueError: If title, description, priority, or tags don't meet validation requirements
        """
        # Validate inputs according to data-model.md
        if not (1 <= len(title) <= 100):
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(title)}")

        if description and not (1 <= len(description) <= 500):
            raise ValueError(f"Description must be between 1 and 500 characters, got {len(description)}")

        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got {priority}")

        if tags is not None:
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError(f"Tags must be non-empty strings, got {tag}")

        # Create new task with unique ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags if tags is not None else set()
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
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    priority: Optional[str] = None, tags: Optional[Set[str]] = None) -> bool:
        """
        Update the title, description, priority, and/or tags of a task by its ID.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            priority: New priority level for the task (optional)
            tags: New set of tags for the task (optional)

        Returns:
            True if the task was successfully updated, False otherwise

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            ValueError: If new values don't meet validation requirements
        """
        task = self.get_task_by_id(task_id)

        # Use existing values if new values are not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description
        new_priority = priority if priority is not None else task.priority
        new_tags = tags if tags is not None else task.tags

        # Validate inputs according to data-model.md
        if not (1 <= len(new_title) <= 100):
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(new_title)}")

        if new_description and not (1 <= len(new_description) <= 500):
            raise ValueError(f"Description must be between 1 and 500 characters, got {len(new_description)}")

        if new_priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got {new_priority}")

        if new_tags is not None:
            for tag in new_tags:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError(f"Tags must be non-empty strings, got {tag}")

        # Update the task
        task.title = new_title
        task.description = new_description
        task.priority = new_priority
        task.tags = new_tags

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

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title, description, or tags.

        Args:
            keyword: The keyword to search for (case-insensitive)

        Returns:
            A list of tasks that contain the keyword in title, description, or tags
        """
        if not keyword:
            return []

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self._tasks:
            # Check if keyword is in title
            if keyword_lower in task.title.lower():
                matching_tasks.append(task)
                continue

            # Check if keyword is in description
            if keyword_lower in task.description.lower():
                matching_tasks.append(task)
                continue

            # Check if keyword is in any of the tags
            for tag in task.tags:
                if keyword_lower in tag.lower():
                    matching_tasks.append(task)
                    break

        return matching_tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, tag: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by status, priority, or tag.

        Args:
            status: Filter by status ('completed' or 'incomplete')
            priority: Filter by priority ('High', 'Medium', 'Low')
            tag: Filter by tag (task must have this tag)

        Returns:
            A list of tasks that match the filter criteria
        """
        filtered_tasks = []

        for task in self._tasks:
            # Check status filter
            if status is not None:
                if status.lower() == 'completed' and not task.completed:
                    continue
                elif status.lower() == 'incomplete' and task.completed:
                    continue

            # Check priority filter
            if priority is not None:
                if priority != task.priority:
                    continue

            # Check tag filter
            if tag is not None:
                if tag not in task.tags:
                    continue

            filtered_tasks.append(task)

        return filtered_tasks

    def sort_tasks(self, sort_by: str) -> List[Task]:
        """
        Sort tasks by the specified field.

        Args:
            sort_by: Field to sort by ('priority', 'status', 'title')

        Returns:
            A list of tasks sorted by the specified field
        """
        if sort_by.lower() == 'priority':
            # Sort by priority: High -> Medium -> Low
            priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
            return sorted(self._tasks, key=lambda task: priority_order[task.priority])
        elif sort_by.lower() == 'status':
            # Sort by status: Incomplete -> Complete
            return sorted(self._tasks, key=lambda task: task.completed)
        elif sort_by.lower() == 'title':
            # Sort by title alphabetically
            return sorted(self._tasks, key=lambda task: task.title.lower())
        else:
            # Return unsorted if sort_by is not recognized
            return self._tasks.copy()