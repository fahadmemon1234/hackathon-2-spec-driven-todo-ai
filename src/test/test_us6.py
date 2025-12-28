"""
Tests for User Story 6: Sort Tasks
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager


class TestUserStory6:
    """Test class for User Story 6: Sort Tasks"""

    def test_sort_by_priority_high_to_low(self):
        """Test sorting tasks by priority from High to Low"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities
        # Add in random order to test sorting
        todo_manager.add_task(title="Low Priority Task", description="Less important", priority="Low")
        todo_manager.add_task(title="High Priority Task", description="Very important", priority="High")
        todo_manager.add_task(title="Medium Priority Task", description="Moderately important", priority="Medium")
        
        # Sort by priority
        sorted_tasks = todo_manager.sort_tasks("priority")
        
        # Check that tasks are sorted from High to Low priority
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].priority == "High"
        assert sorted_tasks[0].title == "High Priority Task"
        assert sorted_tasks[1].priority == "Medium"
        assert sorted_tasks[1].title == "Medium Priority Task"
        assert sorted_tasks[2].priority == "Low"
        assert sorted_tasks[2].title == "Low Priority Task"

    def test_sort_by_priority_all_same_priority(self):
        """Test sorting tasks when all have the same priority"""
        todo_manager = TodoManager()
        
        # Add tasks with the same priority but different titles
        todo_manager.add_task(title="Zebra Task", description="Last alphabetically", priority="High")
        todo_manager.add_task(title="Alpha Task", description="First alphabetically", priority="High")
        todo_manager.add_task(title="Beta Task", description="Middle alphabetically", priority="High")
        
        # Sort by priority
        sorted_tasks = todo_manager.sort_tasks("priority")
        
        # All tasks have the same priority, so order might be based on insertion order
        assert len(sorted_tasks) == 3
        assert all(task.priority == "High" for task in sorted_tasks)

    def test_sort_by_status_incomplete_first(self):
        """Test sorting tasks by status (Incomplete first, then Complete)"""
        todo_manager = TodoManager()
        
        # Add tasks with different completion statuses
        task1_id = todo_manager.add_task(title="Incomplete Task", description="Not done", priority="Medium")
        task2_id = todo_manager.add_task(title="Another Incomplete Task", description="Also not done", priority="Low")
        task3_id = todo_manager.add_task(title="Completed Task", description="Done", priority="High")
        
        # Mark one task as complete
        todo_manager.mark_complete(task3_id)
        
        # Sort by status
        sorted_tasks = todo_manager.sort_tasks("status")
        
        # Check that incomplete tasks come first, then complete tasks
        assert len(sorted_tasks) == 3
        # First two should be incomplete
        assert sorted_tasks[0].completed is False
        assert sorted_tasks[1].completed is False
        # Last one should be complete
        assert sorted_tasks[2].completed is True

    def test_sort_by_title_alphabetically(self):
        """Test sorting tasks by title alphabetically"""
        todo_manager = TodoManager()
        
        # Add tasks with titles that will sort differently alphabetically
        todo_manager.add_task(title="Zebra Task", description="Last alphabetically", priority="Low")
        todo_manager.add_task(title="Alpha Task", description="First alphabetically", priority="High")
        todo_manager.add_task(title="Beta Task", description="Middle alphabetically", priority="Medium")
        todo_manager.add_task(title="Gamma Task", description="Another middle", priority="Low")
        
        # Sort by title
        sorted_tasks = todo_manager.sort_tasks("title")
        
        # Check that tasks are sorted alphabetically by title
        assert len(sorted_tasks) == 4
        expected_order = ["Alpha Task", "Beta Task", "Gamma Task", "Zebra Task"]
        actual_order = [task.title for task in sorted_tasks]
        assert actual_order == expected_order

    def test_sort_by_title_case_insensitive(self):
        """Test that title sorting is case-insensitive"""
        todo_manager = TodoManager()
        
        # Add tasks with mixed case titles
        todo_manager.add_task(title="zebra task", description="Lowercase", priority="Low")
        todo_manager.add_task(title="Alpha Task", description="Capitalized", priority="High")
        todo_manager.add_task(title="beta task", description="Lowercase", priority="Medium")
        
        # Sort by title
        sorted_tasks = todo_manager.sort_tasks("title")
        
        # Check that tasks are sorted alphabetically by title, case-insensitive
        assert len(sorted_tasks) == 3
        expected_order = ["Alpha Task", "beta task", "zebra task"]
        actual_order = [task.title for task in sorted_tasks]
        assert actual_order == expected_order

    def test_sort_with_mixed_completion_status(self):
        """Test sorting by status with various completion states"""
        todo_manager = TodoManager()
        
        # Add tasks with different completion statuses
        task_ids = []
        for i in range(5):
            task_id = todo_manager.add_task(title=f"Task {i}", description=f"Task {i}", priority="Medium")
            task_ids.append(task_id)
        
        # Mark some tasks as complete in a non-sequential way
        todo_manager.mark_complete(task_ids[1])  # Task 1
        todo_manager.mark_complete(task_ids[3])  # Task 3
        
        # Sort by status
        sorted_tasks = todo_manager.sort_tasks("status")
        
        # Verify that incomplete tasks come first, then complete tasks
        assert len(sorted_tasks) == 5
        
        # First should be incomplete (Task 0)
        assert sorted_tasks[0].completed is False
        assert sorted_tasks[0].title == "Task 0"
        
        # Second should be incomplete (Task 2)
        assert sorted_tasks[1].completed is False
        assert sorted_tasks[1].title == "Task 2"
        
        # Third should be incomplete (Task 4)
        assert sorted_tasks[2].completed is False
        assert sorted_tasks[2].title == "Task 4"
        
        # Fourth and fifth should be complete (Tasks 1 and 3)
        assert sorted_tasks[3].completed is True
        assert sorted_tasks[4].completed is True

    def test_sort_empty_list(self):
        """Test sorting an empty list of tasks"""
        todo_manager = TodoManager()
        
        # Sort an empty list
        sorted_tasks = todo_manager.sort_tasks("priority")
        
        # Should return an empty list
        assert len(sorted_tasks) == 0

    def test_sort_single_task(self):
        """Test sorting a list with a single task"""
        todo_manager = TodoManager()
        
        # Add a single task
        todo_manager.add_task(title="Single Task", description="Only task", priority="Medium")
        
        # Sort by priority
        sorted_tasks = todo_manager.sort_tasks("priority")
        
        # Should return the same single task
        assert len(sorted_tasks) == 1
        assert sorted_tasks[0].title == "Single Task"

    def test_sort_invalid_sort_by(self):
        """Test sorting with an invalid sort_by parameter"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Task 1", description="First task", priority="High")
        todo_manager.add_task(title="Task 2", description="Second task", priority="Low")
        
        # Sort with invalid parameter - should return unsorted list
        sorted_tasks = todo_manager.sort_tasks("invalid")
        
        # Should return the tasks in their original order
        assert len(sorted_tasks) == 2

    def test_sort_consistency(self):
        """Test that sorting is consistent across multiple calls"""
        todo_manager = TodoManager()
        
        # Add tasks in a specific order
        todo_manager.add_task(title="Z Task", description="Last", priority="Low")
        todo_manager.add_task(title="A Task", description="First", priority="High")
        todo_manager.add_task(title="M Task", description="Middle", priority="Medium")
        
        # Sort by title multiple times
        sorted_tasks_1 = todo_manager.sort_tasks("title")
        sorted_tasks_2 = todo_manager.sort_tasks("title")
        
        # Both results should be identical
        titles_1 = [task.title for task in sorted_tasks_1]
        titles_2 = [task.title for task in sorted_tasks_2]
        assert titles_1 == titles_2
        assert titles_1 == ["A Task", "M Task", "Z Task"]