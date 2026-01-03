"""
Tests for User Story 1: Enhanced Task Creation with Priority and Tags
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager, TaskNotFoundError


class TestUserStory1:
    """Test class for User Story 1: Enhanced Task Creation with Priority and Tags"""

    def test_create_task_with_priority_and_tags(self):
        """Test creating a task with priority and tags"""
        todo_manager = TodoManager()
        
        # Create a task with priority and tags
        task_id = todo_manager.add_task(
            title="Test Task",
            description="Test Description",
            priority="High",
            tags={"work", "important"}
        )
        
        # Verify the task was created with the correct attributes
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "High"
        assert task.tags == {"work", "important"}
        assert task.completed is False  # Default value

    def test_create_task_with_default_priority_and_tags(self):
        """Test creating a task with default priority and empty tags"""
        todo_manager = TodoManager()
        
        # Create a task without specifying priority and tags (should use defaults)
        task_id = todo_manager.add_task(
            title="Test Task",
            description="Test Description"
        )
        
        # Verify the task was created with default values
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "Medium"  # Default priority
        assert task.tags == set()  # Default empty tags set
        assert task.completed is False  # Default value

    def test_create_task_with_different_priorities(self):
        """Test creating tasks with different priority levels"""
        todo_manager = TodoManager()
        
        # Test High priority
        high_task_id = todo_manager.add_task(
            title="High Priority Task",
            priority="High",
            tags={"urgent"}
        )
        high_task = todo_manager.get_task_by_id(high_task_id)
        assert high_task.priority == "High"
        assert "urgent" in high_task.tags

        # Test Medium priority
        medium_task_id = todo_manager.add_task(
            title="Medium Priority Task",
            priority="Medium",
            tags={"normal"}
        )
        medium_task = todo_manager.get_task_by_id(medium_task_id)
        assert medium_task.priority == "Medium"
        assert "normal" in medium_task.tags

        # Test Low priority
        low_task_id = todo_manager.add_task(
            title="Low Priority Task",
            priority="Low",
            tags={"later"}
        )
        low_task = todo_manager.get_task_by_id(low_task_id)
        assert low_task.priority == "Low"
        assert "later" in low_task.tags

    def test_create_task_with_multiple_tags(self):
        """Test creating a task with multiple tags"""
        todo_manager = TodoManager()
        
        tags = {"work", "important", "deadline", "project"}
        task_id = todo_manager.add_task(
            title="Multi-tag Task",
            tags=tags
        )
        
        task = todo_manager.get_task_by_id(task_id)
        assert task.tags == tags

    def test_create_task_with_empty_tags_set(self):
        """Test creating a task with an explicitly empty tags set"""
        todo_manager = TodoManager()
        
        task_id = todo_manager.add_task(
            title="Empty Tags Task",
            tags=set()
        )
        
        task = todo_manager.get_task_by_id(task_id)
        assert task.tags == set()

    def test_create_task_with_single_tag(self):
        """Test creating a task with a single tag"""
        todo_manager = TodoManager()
        
        task_id = todo_manager.add_task(
            title="Single Tag Task",
            tags={"personal"}
        )
        
        task = todo_manager.get_task_by_id(task_id)
        assert task.tags == {"personal"}

    def test_validation_for_invalid_priority(self):
        """Test that creating a task with invalid priority raises ValueError"""
        todo_manager = TodoManager()
        
        # Try to create a task with an invalid priority
        with pytest.raises(ValueError, match="Priority must be one of"):
            todo_manager.add_task(
                title="Invalid Priority Task",
                priority="InvalidPriority"
            )

    def test_validation_for_invalid_tags(self):
        """Test that creating a task with invalid tags raises ValueError"""
        todo_manager = TodoManager()
        
        # Try to create a task with an invalid tag (empty string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.add_task(
                title="Invalid Tags Task",
                tags={"valid_tag", ""}  # Empty string tag is invalid
            )
        
        # Try to create a task with an invalid tag (not a string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.add_task(
                title="Invalid Tags Task",
                tags={"valid_tag", 123}  # Non-string tag is invalid
            )

    def test_task_creation_preserves_all_attributes(self):
        """Test that all attributes are preserved when creating a task"""
        todo_manager = TodoManager()
        
        task_id = todo_manager.add_task(
            title="Complete Task",
            description="A task with all attributes set",
            priority="High",
            tags={"work", "important", "urgent"}
        )
        
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Complete Task"
        assert task.description == "A task with all attributes set"
        assert task.completed is False  # Default value
        assert task.priority == "High"
        assert task.tags == {"work", "important", "urgent"}