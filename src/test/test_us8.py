"""
Tests for User Story 8: Error Handling and Validation
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager, TaskNotFoundError
from src.models.priority import VALID_PRIORITIES


class TestUserStory8:
    """Test class for User Story 8: Error Handling and Validation"""

    def test_invalid_priority_validation(self):
        """Test validation for invalid priority values"""
        todo_manager = TodoManager()
        
        # Try to add a task with an invalid priority
        with pytest.raises(ValueError, match="Priority must be one of"):
            todo_manager.add_task(
                title="Test Task",
                priority="InvalidPriority"
            )
        
        # Try to update a task with an invalid priority
        task_id = todo_manager.add_task(title="Valid Task", priority="Medium")
        with pytest.raises(ValueError, match="Priority must be one of"):
            todo_manager.update_task(
                task_id=task_id,
                priority="InvalidPriority"
            )

    def test_invalid_tags_validation(self):
        """Test validation for invalid tags"""
        todo_manager = TodoManager()
        
        # Try to add a task with an invalid tag (empty string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.add_task(
                title="Test Task",
                tags={"valid_tag", ""}  # Empty string tag is invalid
            )
        
        # Try to add a task with an invalid tag (not a string)
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.add_task(
                title="Test Task",
                tags={"valid_tag", 123}  # Non-string tag is invalid
            )
        
        # Try to update a task with invalid tags
        task_id = todo_manager.add_task(title="Valid Task", tags={"valid"})
        with pytest.raises(ValueError, match="Tags must be non-empty strings"):
            todo_manager.update_task(
                task_id=task_id,
                tags={"valid", ""}  # Empty string tag is invalid
            )

    def test_invalid_task_id_validation(self):
        """Test validation for invalid task IDs"""
        todo_manager = TodoManager()
        
        # Try to get a non-existent task
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist"):
            todo_manager.get_task_by_id(999)
        
        # Try to update a non-existent task
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist"):
            todo_manager.update_task(task_id=999, title="New Title")
        
        # Try to delete a non-existent task
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist"):
            todo_manager.delete_task(999)
        
        # Try to mark complete a non-existent task
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist"):
            todo_manager.mark_complete(999)
        
        # Try to mark incomplete a non-existent task
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 does not exist"):
            todo_manager.mark_incomplete(999)

    def test_empty_search_results(self):
        """Test handling of search with no results"""
        todo_manager = TodoManager()
        
        # Add a task
        todo_manager.add_task(title="Test Task", description="Test Description", tags={"test"})
        
        # Search for something that doesn't exist
        results = todo_manager.search_tasks("nonexistent")
        assert len(results) == 0

    def test_empty_filter_results(self):
        """Test handling of filter with no results"""
        todo_manager = TodoManager()
        
        # Add a task
        todo_manager.add_task(title="Test Task", description="Test Description", priority="High", tags={"test"})
        
        # Filter by a non-existent tag
        results = todo_manager.filter_tasks(tag="nonexistent")
        assert len(results) == 0
        
        # Filter by a non-existent priority
        results = todo_manager.filter_tasks(priority="NonExistent")
        assert len(results) == 0
        
        # Filter by completed status when all tasks are incomplete
        results = todo_manager.filter_tasks(status="completed")
        assert len(results) == 0

    def test_invalid_title_validation(self):
        """Test validation for invalid titles"""
        todo_manager = TodoManager()
        
        # Try to add a task with an empty title
        with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
            todo_manager.add_task(title="")
        
        # Try to add a task with a title that's too long
        long_title = "x" * 101  # 101 characters
        with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
            todo_manager.add_task(title=long_title)
        
        # Try to update a task with an invalid title
        task_id = todo_manager.add_task(title="Valid Title")
        with pytest.raises(ValueError, match="Title must be between 1 and 100 characters"):
            todo_manager.update_task(task_id=task_id, title="")

    def test_invalid_description_validation(self):
        """Test validation for invalid descriptions"""
        todo_manager = TodoManager()
        
        # Try to add a task with a description that's too long
        long_description = "x" * 501  # 501 characters
        with pytest.raises(ValueError, match="Description must be between 1 and 500 characters"):
            todo_manager.add_task(title="Test Task", description=long_description)
        
        # Try to update a task with an invalid description
        task_id = todo_manager.add_task(title="Valid Task", description="Valid Description")
        long_description = "x" * 501  # 501 characters
        with pytest.raises(ValueError, match="Description must be between 1 and 500 characters"):
            todo_manager.update_task(task_id=task_id, description=long_description)

    def test_edge_case_empty_keyword_search(self):
        """Test searching with empty keyword"""
        todo_manager = TodoManager()
        
        # Add a task
        todo_manager.add_task(title="Test Task", description="Test Description", tags={"test"})
        
        # Search with empty string
        results = todo_manager.search_tasks("")
        assert len(results) == 0

    def test_edge_case_none_values_in_filter(self):
        """Test filtering with None values"""
        todo_manager = TodoManager()
        
        # Add tasks
        todo_manager.add_task(title="Test Task", description="Test Description", priority="High", tags={"test"})
        
        # Filter with None values (should not filter by that criterion)
        results = todo_manager.filter_tasks(priority=None)
        assert len(results) == 1
        
        results = todo_manager.filter_tasks(status=None)
        assert len(results) == 1
        
        results = todo_manager.filter_tasks(tag=None)
        assert len(results) == 1

    def test_error_message_formatting(self):
        """Test that error messages are properly formatted"""
        todo_manager = TodoManager()
        
        # Test priority error message
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(title="Test", priority="Invalid")
        error_msg = str(exc_info.value)
        assert "Priority must be one of" in error_msg
        for priority in VALID_PRIORITIES:
            assert priority in error_msg
        
        # Test tag error message
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(title="Test", tags={"valid", ""})
        error_msg = str(exc_info.value)
        assert "Tags must be non-empty strings" in error_msg
        
        # Test title error message
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(title="")  # Empty title
        error_msg = str(exc_info.value)
        assert "Title must be between 1 and 100 characters" in error_msg
        
        # Test description error message
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(title="Test", description="x" * 501)  # Too long
        error_msg = str(exc_info.value)
        assert "Description must be between 1 and 500 characters" in error_msg

    def test_multiple_validation_errors(self):
        """Test handling of multiple validation errors in one operation"""
        todo_manager = TodoManager()
        
        # Try to add a task with multiple validation issues
        with pytest.raises(ValueError):
            todo_manager.add_task(
                title="",  # Invalid title
                priority="InvalidPriority",  # Invalid priority
                tags={"valid", ""}  # Invalid tag
            )