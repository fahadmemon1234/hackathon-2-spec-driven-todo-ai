"""
Tests for User Story 2: Enhanced Task Update with Priority and Tags
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager, TaskNotFoundError


class TestUserStory2:
    """Test class for User Story 2: Enhanced Task Update with Priority and Tags"""

    def test_update_task_priority_only(self):
        """Test updating only the priority of a task"""
        todo_manager = TodoManager()
        
        # Create a task with initial priority
        task_id = todo_manager.add_task(
            title="Test Task",
            description="Test Description",
            priority="Low",
            tags={"work"}
        )
        
        # Update only the priority
        success = todo_manager.update_task(
            task_id=task_id,
            priority="High"
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"  # Should remain unchanged
        assert task.description == "Test Description"  # Should remain unchanged
        assert task.priority == "High"  # Should be updated
        assert task.tags == {"work"}  # Should remain unchanged
        assert task.completed is False  # Should remain unchanged

    def test_update_task_tags_only(self):
        """Test updating only the tags of a task"""
        todo_manager = TodoManager()
        
        # Create a task with initial tags
        task_id = todo_manager.add_task(
            title="Test Task",
            description="Test Description",
            priority="Medium",
            tags={"work", "important"}
        )
        
        # Update only the tags
        new_tags = {"personal", "home"}
        success = todo_manager.update_task(
            task_id=task_id,
            tags=new_tags
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"  # Should remain unchanged
        assert task.description == "Test Description"  # Should remain unchanged
        assert task.priority == "Medium"  # Should remain unchanged
        assert task.tags == new_tags  # Should be updated
        assert task.completed is False  # Should remain unchanged

    def test_update_task_priority_and_tags(self):
        """Test updating both priority and tags of a task"""
        todo_manager = TodoManager()
        
        # Create a task with initial values
        task_id = todo_manager.add_task(
            title="Test Task",
            description="Test Description",
            priority="Low",
            tags={"work"}
        )
        
        # Update both priority and tags
        new_tags = {"personal", "home", "urgent"}
        success = todo_manager.update_task(
            task_id=task_id,
            priority="High",
            tags=new_tags
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"  # Should remain unchanged
        assert task.description == "Test Description"  # Should remain unchanged
        assert task.priority == "High"  # Should be updated
        assert task.tags == new_tags  # Should be updated
        assert task.completed is False  # Should remain unchanged

    def test_update_task_title_and_priority(self):
        """Test updating title and priority while keeping tags unchanged"""
        todo_manager = TodoManager()
        
        # Create a task with initial values
        task_id = todo_manager.add_task(
            title="Old Title",
            description="Test Description",
            priority="Low",
            tags={"work", "important"}
        )
        
        # Update title and priority
        success = todo_manager.update_task(
            task_id=task_id,
            title="New Title",
            priority="High"
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "New Title"  # Should be updated
        assert task.description == "Test Description"  # Should remain unchanged
        assert task.priority == "High"  # Should be updated
        assert task.tags == {"work", "important"}  # Should remain unchanged
        assert task.completed is False  # Should remain unchanged

    def test_update_task_description_and_tags(self):
        """Test updating description and tags while keeping priority unchanged"""
        todo_manager = TodoManager()
        
        # Create a task with initial values
        task_id = todo_manager.add_task(
            title="Test Title",
            description="Old Description",
            priority="Medium",
            tags={"work"}
        )
        
        # Update description and tags
        new_tags = {"personal", "home"}
        success = todo_manager.update_task(
            task_id=task_id,
            description="New Description",
            tags=new_tags
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Title"  # Should remain unchanged
        assert task.description == "New Description"  # Should be updated
        assert task.priority == "Medium"  # Should remain unchanged
        assert task.tags == new_tags  # Should be updated
        assert task.completed is False  # Should remain unchanged

    def test_update_task_all_attributes(self):
        """Test updating all attributes of a task"""
        todo_manager = TodoManager()
        
        # Create a task with initial values
        task_id = todo_manager.add_task(
            title="Old Title",
            description="Old Description",
            priority="Low",
            tags={"work"}
        )
        
        # Update all attributes
        new_tags = {"personal", "home", "urgent", "important"}
        success = todo_manager.update_task(
            task_id=task_id,
            title="New Title",
            description="New Description",
            priority="High",
            tags=new_tags
        )
        
        assert success is True
        
        # Verify the task was updated correctly
        task = todo_manager.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "New Title"  # Should be updated
        assert task.description == "New Description"  # Should be updated
        assert task.priority == "High"  # Should be updated
        assert task.tags == new_tags  # Should be updated
        assert task.completed is False  # Should remain unchanged

    def test_update_task_with_invalid_priority(self):
        """Test that updating a task with invalid priority raises ValueError"""
        todo_manager = TodoManager()
        
        # Create a task
        task_id = todo_manager.add_task(
            title="Test Task",
            priority="Medium"
        )
        
        # Try to update with invalid priority
        with pytest.raises(ValueError, match="Priority must be one of"):
            todo_manager.update_task(
                task_id=task_id,
                priority="InvalidPriority"
            )

    def test_update_task_with_invalid_tags(self):
        """Test that updating a task with invalid tags raises ValueError"""
        todo_manager = TodoManager()
        
        # Create a task
        task_id = todo_manager.add_task(
            title="Test Task",
            tags={"valid_tag"}
        )
        
        # Try to update with invalid tags (empty string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.update_task(
                task_id=task_id,
                tags={"valid_tag", ""}
            )
        
        # Try to update with invalid tags (non-string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.update_task(
                task_id=task_id,
                tags={"valid_tag", 123}
            )

    def test_update_nonexistent_task(self):
        """Test that updating a non-existent task raises TaskNotFoundError"""
        todo_manager = TodoManager()
        
        # Try to update a task that doesn't exist
        with pytest.raises(TaskNotFoundError):
            todo_manager.update_task(
                task_id=999,  # Non-existent ID
                priority="High"
            )

    def test_partial_update_preserves_unspecified_attributes(self):
        """Test that unspecified attributes remain unchanged during partial updates"""
        todo_manager = TodoManager()
        
        # Create a task with specific values
        task_id = todo_manager.add_task(
            title="Original Title",
            description="Original Description",
            priority="Low",
            tags={"original", "tag"}
        )
        
        # Update only the title
        success = todo_manager.update_task(
            task_id=task_id,
            title="Updated Title"
        )
        
        assert success is True
        
        # Verify only title changed, other attributes preserved
        task = todo_manager.get_task_by_id(task_id)
        assert task.title == "Updated Title"  # Updated
        assert task.description == "Original Description"  # Preserved
        assert task.priority == "Low"  # Preserved
        assert task.tags == {"original", "tag"}  # Preserved