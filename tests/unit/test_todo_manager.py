import pytest
from src.services.todo_manager import TodoManager, TaskNotFoundError
from src.models.task import Task


def test_add_task():
    """Test adding a task to the TodoManager."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Title", "Test Description")
    
    assert task_id == 1
    assert len(manager.get_all_tasks()) == 1
    
    task = manager.get_all_tasks()[0]
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is False


def test_add_task_defaults():
    """Test adding a task with only a title."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Title")
    
    assert task_id == 1
    assert len(manager.get_all_tasks()) == 1
    
    task = manager.get_all_tasks()[0]
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == ""
    assert task.completed is False


def test_add_task_validation():
    """Test validation when adding tasks."""
    manager = TodoManager()
    
    # Title too short
    with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
        manager.add_task("")
    
    # Title too long
    with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
        manager.add_task("A" * 101)
    
    # Description too long
    with pytest.raises(ValueError, match="Description must be between 1 and 500 characters"):
        manager.add_task("Test", "A" * 501)


def test_get_all_tasks():
    """Test getting all tasks."""
    manager = TodoManager()
    
    # Initially empty
    assert len(manager.get_all_tasks()) == 0
    
    # After adding tasks
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")
    
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_task_by_id():
    """Test getting a task by its ID."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Task", "Test Description")
    
    task = manager.get_task_by_id(task_id)
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"


def test_get_task_by_id_not_found():
    """Test getting a task that doesn't exist."""
    manager = TodoManager()
    
    with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist."):
        manager.get_task_by_id(999)


def test_update_task():
    """Test updating a task."""
    manager = TodoManager()
    
    task_id = manager.add_task("Original Title", "Original Description")
    
    result = manager.update_task(task_id, "New Title", "New Description")
    
    assert result is True
    
    updated_task = manager.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_partial():
    """Test updating only title or description."""
    manager = TodoManager()
    
    task_id = manager.add_task("Original Title", "Original Description")
    
    # Update only title
    manager.update_task(task_id, title="New Title")
    
    updated_task = manager.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"
    
    # Update only description
    manager.update_task(task_id, description="New Description")
    
    updated_task = manager.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_not_found():
    """Test updating a task that doesn't exist."""
    manager = TodoManager()
    
    with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist."):
        manager.update_task(999, "New Title", "New Description")


def test_update_task_validation():
    """Test validation when updating tasks."""
    manager = TodoManager()
    
    task_id = manager.add_task("Original Title", "Original Description")
    
    # Title too long
    with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
        manager.update_task(task_id, "A" * 101, "New Description")


def test_delete_task():
    """Test deleting a task."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Task", "Test Description")
    
    result = manager.delete_task(task_id)
    
    assert result is True
    assert len(manager.get_all_tasks()) == 0


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist."""
    manager = TodoManager()
    
    with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist."):
        manager.delete_task(999)


def test_mark_complete():
    """Test marking a task as complete."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Task", "Test Description")
    
    result = manager.mark_complete(task_id)
    
    assert result is True
    
    task = manager.get_task_by_id(task_id)
    assert task.completed is True


def test_mark_complete_not_found():
    """Test marking a task as complete when it doesn't exist."""
    manager = TodoManager()
    
    with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist."):
        manager.mark_complete(999)


def test_mark_incomplete():
    """Test marking a task as incomplete."""
    manager = TodoManager()
    
    task_id = manager.add_task("Test Task", "Test Description")
    
    # First mark as complete
    manager.mark_complete(task_id)
    
    # Then mark as incomplete
    result = manager.mark_incomplete(task_id)
    
    assert result is True
    
    task = manager.get_task_by_id(task_id)
    assert task.completed is False


def test_mark_incomplete_not_found():
    """Test marking a task as incomplete when it doesn't exist."""
    manager = TodoManager()
    
    with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist."):
        manager.mark_incomplete(999)


def test_id_generation():
    """Test that IDs are generated sequentially."""
    manager = TodoManager()
    
    id1 = manager.add_task("Task 1", "Description 1")
    id2 = manager.add_task("Task 2", "Description 2")
    id3 = manager.add_task("Task 3", "Description 3")
    
    assert id1 == 1
    assert id2 == 2
    assert id3 == 3