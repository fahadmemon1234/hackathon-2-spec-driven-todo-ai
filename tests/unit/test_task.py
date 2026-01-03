import pytest
from src.models.task import Task


def test_task_creation():
    """Test that a Task can be created with valid parameters."""
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_task_creation_defaults():
    """Test that a Task can be created with default completion status."""
    task = Task(id=1, title="Test Task", description="Test Description")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False  # Default value


def test_task_title_length_validation():
    """Test that Task validates title length."""
    # Valid title
    Task(id=1, title="A", description="Test Description")  # Min length
    Task(id=1, title="A" * 100, description="Test Description")  # Max length
    
    # Invalid titles
    with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
        Task(id=1, title="", description="Test Description")  # Too short
    
    with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
        Task(id=1, title="A" * 101, description="Test Description")  # Too long


def test_task_description_length_validation():
    """Test that Task validates description length."""
    # Valid descriptions
    Task(id=1, title="Test", description="A")  # Min length
    Task(id=1, title="Test", description="A" * 500)  # Max length
    Task(id=1, title="Test", description="")  # Empty description is allowed
    
    # Invalid descriptions
    with pytest.raises(ValueError, match="Description must be between 1 and 500 characters"):
        Task(id=1, title="Test", description="A" * 501)  # Too long


def test_task_id_validation():
    """Test that Task validates ID is positive."""
    # Valid ID
    Task(id=1, title="Test Task", description="Test Description")
    
    # Invalid IDs
    with pytest.raises(ValueError, match="ID must be a positive integer"):
        Task(id=0, title="Test Task", description="Test Description")
    
    with pytest.raises(ValueError, match="ID must be a positive integer"):
        Task(id=-1, title="Test Task", description="Test Description")


def test_task_completed_validation():
    """Test that Task validates completed status is boolean."""
    # Valid completed status
    Task(id=1, title="Test Task", description="Test Description", completed=True)
    Task(id=1, title="Test Task", description="Test Description", completed=False)
    
    # Invalid completed status
    with pytest.raises(ValueError, match="Completed status must be a boolean value"):
        Task(id=1, title="Test Task", description="Test Description", completed="True")
    
    with pytest.raises(ValueError, match="Completed status must be a boolean value"):
        Task(id=1, title="Test Task", description="Test Description", completed=1)