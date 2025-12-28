"""
Tests for User Story 7: CLI Enhancement and Integration
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager


class TestUserStory7:
    """Test class for User Story 7: CLI Enhancement and Integration"""

    def test_combined_search_and_filter_by_status(self):
        """Test combining search and filter by status"""
        todo_manager = TodoManager()
        
        # Add tasks with different statuses and content
        task1_id = todo_manager.add_task(
            title="Work on API documentation", 
            description="Create documentation for the new API", 
            priority="High", 
            tags={"work", "documentation"}
        )
        task2_id = todo_manager.add_task(
            title="Buy groceries", 
            description="Get milk and bread", 
            priority="Medium", 
            tags={"shopping", "food"}
        )
        task3_id = todo_manager.add_task(
            title="Fix urgent bug", 
            description="Resolve critical system bug", 
            priority="High", 
            tags={"work", "bug", "urgent"}
        )
        
        # Mark one task as complete
        todo_manager.mark_complete(task1_id)
        
        # Search for "work" and filter by completed status
        search_results = todo_manager.search_tasks("work")
        filtered_results = [task for task in search_results if task.completed]
        
        assert len(filtered_results) == 1
        assert filtered_results[0].title == "Work on API documentation"
        assert filtered_results[0].completed is True

    def test_combined_search_and_filter_by_priority(self):
        """Test combining search and filter by priority"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities and content
        todo_manager.add_task(
            title="Low priority task", 
            description="Not very important", 
            priority="Low", 
            tags={"low", "later"}
        )
        todo_manager.add_task(
            title="High priority work task", 
            description="Very important work", 
            priority="High", 
            tags={"work", "urgent"}
        )
        todo_manager.add_task(
            title="Medium priority work task", 
            description="Moderately important work", 
            priority="Medium", 
            tags={"work", "normal"}
        )
        
        # Search for "work" and filter by high priority
        search_results = todo_manager.search_tasks("work")
        filtered_results = [task for task in search_results if task.priority == "High"]
        
        assert len(filtered_results) == 1
        assert filtered_results[0].title == "High priority work task"
        assert filtered_results[0].priority == "High"

    def test_combined_search_and_filter_by_tag(self):
        """Test combining search and filter by tag"""
        todo_manager = TodoManager()
        
        # Add tasks with different tags and content
        todo_manager.add_task(
            title="Work task", 
            description="General work task", 
            priority="Medium", 
            tags={"work", "normal"}
        )
        todo_manager.add_task(
            title="Urgent work task", 
            description="Urgent work item", 
            priority="High", 
            tags={"work", "urgent"}
        )
        todo_manager.add_task(
            title="Personal task", 
            description="Personal stuff", 
            priority="Low", 
            tags={"personal", "home"}
        )
        
        # Search for "work" in title and filter by "urgent" tag
        search_results = todo_manager.search_tasks("work")
        filtered_results = [task for task in search_results if "urgent" in task.tags]
        
        assert len(filtered_results) == 1
        assert filtered_results[0].title == "Urgent work task"
        assert "urgent" in filtered_results[0].tags

    def test_combined_sort_and_filter(self):
        """Test combining sort and filter operations"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities and statuses
        task1_id = todo_manager.add_task(
            title="Low priority incomplete", 
            description="Not important", 
            priority="Low", 
            tags={"low"}
        )
        task2_id = todo_manager.add_task(
            title="High priority complete", 
            description="Very important", 
            priority="High", 
            tags={"high"}
        )
        task3_id = todo_manager.add_task(
            title="Medium priority incomplete", 
            description="Moderately important", 
            priority="Medium", 
            tags={"medium"}
        )
        
        # Mark tasks as complete
        todo_manager.mark_complete(task2_id)
        
        # Filter by incomplete status first
        filtered_tasks = todo_manager.filter_tasks(status="incomplete")
        
        # Then sort the filtered results by priority
        sorted_filtered_tasks = sorted(
            filtered_tasks, 
            key=lambda task: {"High": 1, "Medium": 2, "Low": 3}[task.priority]
        )
        
        assert len(sorted_filtered_tasks) == 2
        assert sorted_filtered_tasks[0].priority == "Medium"  # Medium priority incomplete task
        assert sorted_filtered_tasks[1].priority == "Low"    # Low priority incomplete task

    def test_combined_search_filter_and_sort(self):
        """Test combining search, filter, and sort operations"""
        todo_manager = TodoManager()
        
        # Add tasks with various attributes
        todo_manager.add_task(
            title="High priority urgent work", 
            description="Very important work task", 
            priority="High", 
            tags={"work", "urgent", "important"}
        )
        todo_manager.add_task(
            title="Low priority urgent work", 
            description="Less important but urgent work", 
            priority="Low", 
            tags={"work", "urgent"}
        )
        todo_manager.add_task(
            title="Medium priority work", 
            description="Regular work task", 
            priority="Medium", 
            tags={"work", "normal"}
        )
        todo_manager.add_task(
            title="High priority personal", 
            description="Important personal task", 
            priority="High", 
            tags={"personal", "important"}
        )
        
        # First, search for tasks containing "work"
        search_results = todo_manager.search_tasks("work")
        
        # Then, filter for tasks with "urgent" tag
        filtered_results = [task for task in search_results if "urgent" in task.tags]
        
        # Finally, sort by priority (High to Low)
        sorted_results = sorted(
            filtered_results,
            key=lambda task: {"High": 1, "Medium": 2, "Low": 3}[task.priority]
        )
        
        assert len(sorted_results) == 2  # Two tasks with "work" and "urgent"
        
        # First should be High priority
        assert sorted_results[0].title == "High priority urgent work"
        assert sorted_results[0].priority == "High"
        assert "urgent" in sorted_results[0].tags
        
        # Second should be Low priority
        assert sorted_results[1].title == "Low priority urgent work"
        assert sorted_results[1].priority == "Low"
        assert "urgent" in sorted_results[1].tags

    def test_multiple_filters_combined(self):
        """Test applying multiple filters in sequence"""
        todo_manager = TodoManager()
        
        # Add tasks with various attributes
        task1_id = todo_manager.add_task(
            title="Completed high priority", 
            description="Done and important", 
            priority="High", 
            tags={"work", "important"}
        )
        task2_id = todo_manager.add_task(
            title="Incomplete high priority", 
            description="Not done but important", 
            priority="High", 
            tags={"work", "important"}
        )
        task3_id = todo_manager.add_task(
            title="Incomplete low priority", 
            description="Not done and less important", 
            priority="Low", 
            tags={"personal", "later"}
        )
        
        # Mark first task as complete
        todo_manager.mark_complete(task1_id)
        
        # Apply multiple filters: status=completed AND priority=High
        status_filtered = todo_manager.filter_tasks(status="completed")
        final_filtered = [task for task in status_filtered if task.priority == "High"]
        
        assert len(final_filtered) == 1
        assert final_filtered[0].title == "Completed high priority"
        assert final_filtered[0].completed is True
        assert final_filtered[0].priority == "High"

    def test_integration_with_empty_results(self):
        """Test combined operations when they result in empty results"""
        todo_manager = TodoManager()

        # Add some tasks
        todo_manager.add_task(
            title="Work task",
            description="Work related",
            priority="Medium",
            tags={"work"}
        )
        todo_manager.add_task(
            title="Personal task",
            description="Personal stuff",
            priority="Low",
            tags={"personal"}
        )

        # Search for something that doesn't exist
        search_results = todo_manager.search_tasks("nonexistent")
        assert len(search_results) == 0

        # Filter for a tag that doesn't exist
        filter_results = todo_manager.filter_tasks(tag="nonexistent")
        assert len(filter_results) == 0

        # Note: The sort operation will return all tasks in sorted order, not an empty list
        # unless we filter to an empty list first
        sort_results = todo_manager.sort_tasks("priority")
        assert len(sort_results) == 2  # All tasks sorted by priority

    def test_complex_integration_scenario(self):
        """Test a complex scenario combining all operations"""
        todo_manager = TodoManager()
        
        # Add a comprehensive set of tasks
        todo_manager.add_task(
            title="Fix critical API bug", 
            description="System is down, fix immediately", 
            priority="High", 
            tags={"work", "bug", "urgent", "api"}
        )
        todo_manager.add_task(
            title="Write API documentation", 
            description="Document the new API endpoints", 
            priority="Medium", 
            tags={"work", "documentation", "api"}
        )
        todo_manager.add_task(
            title="Buy groceries", 
            description="Get weekly groceries", 
            priority="Low", 
            tags={"shopping", "personal", "food"}
        )
        task4_id = todo_manager.add_task(
            title="Prepare presentation", 
            description="Get ready for team meeting", 
            priority="High", 
            tags={"work", "meeting", "presentation"}
        )
        todo_manager.add_task(
            title="Schedule dentist appointment", 
            description="Book next checkup", 
            priority="Low", 
            tags={"personal", "health"}
        )
        
        # Mark one task as complete
        todo_manager.mark_complete(task4_id)
        
        # Complex operation: Search for "work", filter by incomplete status, sort by priority
        search_results = todo_manager.search_tasks("work")
        filtered_results = [task for task in search_results if not task.completed]
        sorted_results = sorted(
            filtered_results,
            key=lambda task: {"High": 1, "Medium": 2, "Low": 3}[task.priority]
        )
        
        # The work tasks are: "Fix critical API bug", "Write API documentation", "Prepare presentation"
        # Of these, "Prepare presentation" was marked complete, so it should be filtered out
        # So we should have 2 tasks: "Fix critical API bug" (High) and "Write API documentation" (Medium)
        assert len(sorted_results) == 2
        assert sorted_results[0].title == "Fix critical API bug"
        assert sorted_results[0].priority == "High"
        assert sorted_results[1].title == "Write API documentation"
        assert sorted_results[1].priority == "Medium"