"""
Tests for User Story 3: Enhanced Task View
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager
from src.cli.display import format_task_display, format_tasks_list, get_priority_indicator, format_task_brief


class TestUserStory3:
    """Test class for User Story 3: Enhanced Task View"""

    def test_format_task_display(self):
        """Test formatting a single task for display"""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            priority="High",
            tags={"work", "important"}
        )

        formatted = format_task_display(task)

        # Check that all required information is present in the formatted string
        assert "[1]" in formatted
        assert "Test Task" in formatted
        assert "Test Description" in formatted
        assert "Priority: High" in formatted
        assert "work" in formatted
        assert "important" in formatted
        assert "Status: [INCOMPLETE]" in formatted  # [INCOMPLETE] for incomplete

        # Create a completed task
        completed_task = Task(
            id=2,
            title="Completed Task",
            description="Completed Description",
            completed=True,
            priority="Low",
            tags={"personal"}
        )

        formatted_completed = format_task_display(completed_task)
        assert "Status: [COMPLETED]" in formatted_completed  # [COMPLETED] for complete

    def test_format_task_display_with_empty_tags(self):
        """Test formatting a task with no tags"""
        task = Task(
            id=1,
            title="No Tags Task",
            description="Description",
            completed=False,
            priority="Medium",
            tags=set()  # Empty tags
        )
        
        formatted = format_task_display(task)
        assert "Tags: None" in formatted

    def test_format_task_display_with_special_characters(self):
        """Test formatting a task with special characters in title/description"""
        task = Task(
            id=1,
            title="Task with 'quotes' and \"double quotes\"",
            description="Description with special chars: !@#$%^&*()",
            completed=False,
            priority="Medium",
            tags={"special", "chars!"}
        )
        
        formatted = format_task_display(task)
        assert "Task with 'quotes' and \"double quotes\"" in formatted
        assert "Description with special chars: !@#$%^&*()" in formatted

    def test_format_tasks_list(self):
        """Test formatting a list of tasks"""
        tasks = [
            Task(id=1, title="Task 1", description="Description 1", completed=False, priority="High", tags={"work"}),
            Task(id=2, title="Task 2", description="Description 2", completed=True, priority="Low", tags={"personal"}),
        ]
        
        formatted_list = format_tasks_list(tasks)
        
        assert len(formatted_list) == 2
        assert "[1]" in formatted_list[0]
        assert "[2]" in formatted_list[1]
        assert "Task 1" in formatted_list[0]
        assert "Task 2" in formatted_list[1]

    def test_get_priority_indicator(self):
        """Test getting priority indicators"""
        assert get_priority_indicator("High") == "[HIGH]"
        assert get_priority_indicator("Medium") == "[MED]"
        assert get_priority_indicator("Low") == "[LOW]"

        # Test with invalid priority
        assert get_priority_indicator("Invalid") == "[N/A]"

    def test_format_task_brief(self):
        """Test formatting a brief representation of a task"""
        task = Task(
            id=1,
            title="Brief Task",
            description="Description",
            completed=False,
            priority="High",
            tags={"work", "important", "urgent"}
        )
        
        brief = format_task_brief(task)
        
        assert "[1]" in brief
        assert "Brief Task" in brief
        assert "[HIGH]" in brief  # High priority indicator
        assert "[I]" in brief  # Incomplete indicator
        assert "(3 tags)" in brief  # 3 tags count

        # Test with completed task
        task.completed = True
        brief_completed = format_task_brief(task)
        assert "[C]" in brief_completed  # Complete indicator

    def test_display_with_different_priorities(self):
        """Test display formatting with different priority levels"""
        high_task = Task(id=1, title="High Priority", priority="High", tags=set())
        medium_task = Task(id=2, title="Medium Priority", priority="Medium", tags=set())
        low_task = Task(id=3, title="Low Priority", priority="Low", tags=set())

        high_formatted = format_task_display(high_task)
        medium_formatted = format_task_display(medium_task)
        low_formatted = format_task_display(low_task)

        assert "Priority: High" in high_formatted
        assert "Priority: Medium" in medium_formatted
        assert "Priority: Low" in low_formatted

        # Check priority indicators
        assert "[HIGH]" in high_formatted
        assert "[MED]" in medium_formatted
        assert "[LOW]" in low_formatted

    def test_display_with_various_tag_counts(self):
        """Test display formatting with different numbers of tags"""
        # Task with no tags
        no_tags_task = Task(id=1, title="No Tags", tags=set())
        no_tags_formatted = format_task_display(no_tags_task)
        assert "Tags: None" in no_tags_formatted
        
        # Task with one tag
        one_tag_task = Task(id=2, title="One Tag", tags={"single"})
        one_tag_formatted = format_task_display(one_tag_task)
        assert "Tags: single" in one_tag_formatted
        
        # Task with multiple tags
        multi_tag_task = Task(id=3, title="Multi Tags", tags={"first", "second", "third"})
        multi_tag_formatted = format_task_display(multi_tag_task)
        # Tags should be sorted alphabetically
        assert "first, second, third" in multi_tag_formatted

    def test_display_sorting_of_tags(self):
        """Test that tags are displayed in sorted order"""
        task = Task(
            id=1,
            title="Sorted Tags",
            tags={"zebra", "alpha", "beta", "gamma"}
        )
        
        formatted = format_task_display(task)
        # Tags should appear in alphabetical order
        assert "alpha, beta, gamma, zebra" in formatted