"""
Tests for User Story 5: Filter Tasks
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager


class TestUserStory5:
    """Test class for User Story 5: Filter Tasks"""

    def test_filter_by_status_completed(self):
        """Test filtering tasks by completed status"""
        todo_manager = TodoManager()
        
        # Add some tasks with different completion statuses
        task1_id = todo_manager.add_task(title="Completed Task", description="This is done", priority="High")
        task2_id = todo_manager.add_task(title="Incomplete Task", description="This is not done", priority="Medium")
        task3_id = todo_manager.add_task(title="Another Completed Task", description="Also done", priority="Low")
        
        # Mark some tasks as complete
        todo_manager.mark_complete(task1_id)
        todo_manager.mark_complete(task3_id)
        
        # Filter by completed status
        completed_tasks = todo_manager.filter_tasks(status="completed")
        assert len(completed_tasks) == 2
        completed_titles = {task.title for task in completed_tasks}
        assert completed_titles == {"Completed Task", "Another Completed Task"}

    def test_filter_by_status_incomplete(self):
        """Test filtering tasks by incomplete status"""
        todo_manager = TodoManager()
        
        # Add some tasks with different completion statuses
        todo_manager.add_task(title="Completed Task", description="This is done", priority="High")
        todo_manager.add_task(title="Incomplete Task", description="This is not done", priority="Medium")
        todo_manager.add_task(title="Another Incomplete Task", description="Also not done", priority="Low")
        
        # Mark one task as complete
        todo_manager.mark_complete(1)
        
        # Filter by incomplete status
        incomplete_tasks = todo_manager.filter_tasks(status="incomplete")
        assert len(incomplete_tasks) == 2
        incomplete_titles = {task.title for task in incomplete_tasks}
        assert incomplete_titles == {"Incomplete Task", "Another Incomplete Task"}

    def test_filter_by_priority_high(self):
        """Test filtering tasks by high priority"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities
        todo_manager.add_task(title="High Priority Task", description="Important task", priority="High")
        todo_manager.add_task(title="Medium Priority Task", description="Normal task", priority="Medium")
        todo_manager.add_task(title="Low Priority Task", description="Less important task", priority="Low")
        
        # Filter by high priority
        high_priority_tasks = todo_manager.filter_tasks(priority="High")
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].title == "High Priority Task"
        assert high_priority_tasks[0].priority == "High"

    def test_filter_by_priority_medium(self):
        """Test filtering tasks by medium priority"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities
        todo_manager.add_task(title="High Priority Task", description="Important task", priority="High")
        todo_manager.add_task(title="Medium Priority Task 1", description="Normal task", priority="Medium")
        todo_manager.add_task(title="Medium Priority Task 2", description="Another normal task", priority="Medium")
        todo_manager.add_task(title="Low Priority Task", description="Less important task", priority="Low")
        
        # Filter by medium priority
        medium_priority_tasks = todo_manager.filter_tasks(priority="Medium")
        assert len(medium_priority_tasks) == 2
        medium_titles = {task.title for task in medium_priority_tasks}
        assert medium_titles == {"Medium Priority Task 1", "Medium Priority Task 2"}

    def test_filter_by_priority_low(self):
        """Test filtering tasks by low priority"""
        todo_manager = TodoManager()
        
        # Add tasks with different priorities
        todo_manager.add_task(title="High Priority Task", description="Important task", priority="High")
        todo_manager.add_task(title="Medium Priority Task", description="Normal task", priority="Medium")
        todo_manager.add_task(title="Low Priority Task", description="Less important task", priority="Low")
        
        # Filter by low priority
        low_priority_tasks = todo_manager.filter_tasks(priority="Low")
        assert len(low_priority_tasks) == 1
        assert low_priority_tasks[0].title == "Low Priority Task"
        assert low_priority_tasks[0].priority == "Low"

    def test_filter_by_tag(self):
        """Test filtering tasks by tag"""
        todo_manager = TodoManager()
        
        # Add tasks with different tags
        todo_manager.add_task(title="Work Task", description="Work related", tags={"work", "important"})
        todo_manager.add_task(title="Personal Task", description="Personal stuff", tags={"personal", "home"})
        todo_manager.add_task(title="Shopping Task", description="Buy groceries", tags={"shopping", "work"})  # Has both shopping and work tags
        
        # Filter by "work" tag
        work_tasks = todo_manager.filter_tasks(tag="work")
        assert len(work_tasks) == 2
        work_titles = {task.title for task in work_tasks}
        assert work_titles == {"Work Task", "Shopping Task"}  # Shopping Task also has "work" tag

    def test_filter_by_nonexistent_tag(self):
        """Test filtering by a tag that doesn't exist"""
        todo_manager = TodoManager()
        
        # Add tasks with different tags
        todo_manager.add_task(title="Work Task", description="Work related", tags={"work", "important"})
        todo_manager.add_task(title="Personal Task", description="Personal stuff", tags={"personal", "home"})
        
        # Filter by a tag that doesn't exist
        nonexistent_tag_tasks = todo_manager.filter_tasks(tag="nonexistent")
        assert len(nonexistent_tag_tasks) == 0

    def test_filter_by_multiple_criteria(self):
        """Test filtering by multiple criteria simultaneously (status and priority)"""
        todo_manager = TodoManager()
        
        # Add tasks with different statuses and priorities
        task1_id = todo_manager.add_task(title="Completed High Priority", description="Done and important", priority="High")
        todo_manager.add_task(title="Incomplete High Priority", description="Not done but important", priority="High")
        todo_manager.add_task(title="Incomplete Low Priority", description="Not done and less important", priority="Low")
        
        # Mark first task as complete
        todo_manager.mark_complete(task1_id)
        
        # Filter by completed status and high priority
        filtered_tasks = todo_manager.filter_tasks(status="completed", priority="High")
        assert len(filtered_tasks) == 1
        assert filtered_tasks[0].title == "Completed High Priority"
        assert filtered_tasks[0].priority == "High"
        assert filtered_tasks[0].completed is True

    def test_filter_by_status_and_tag(self):
        """Test filtering by status and tag simultaneously"""
        todo_manager = TodoManager()
        
        # Add tasks with different statuses and tags
        task1_id = todo_manager.add_task(title="Completed Work Task", description="Done work", priority="High", tags={"work", "important"})
        todo_manager.add_task(title="Incomplete Work Task", description="Not done work", priority="Medium", tags={"work", "normal"})
        todo_manager.add_task(title="Incomplete Personal Task", description="Not done personal", priority="Low", tags={"personal"})
        
        # Mark first task as complete
        todo_manager.mark_complete(task1_id)
        
        # Filter by completed status and "work" tag
        filtered_tasks = todo_manager.filter_tasks(status="completed", tag="work")
        assert len(filtered_tasks) == 1
        assert filtered_tasks[0].title == "Completed Work Task"
        assert "work" in filtered_tasks[0].tags
        assert filtered_tasks[0].completed is True

    def test_filter_no_matches(self):
        """Test filtering when no tasks match the criteria"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Work Task", description="Work related", priority="High", tags={"work"})
        todo_manager.add_task(title="Personal Task", description="Personal stuff", priority="Low", tags={"personal"})
        
        # Filter by a non-existent priority
        no_match_tasks = todo_manager.filter_tasks(priority="NonExistent")
        assert len(no_match_tasks) == 0
        
        # Filter by a non-existent tag
        no_match_tasks = todo_manager.filter_tasks(tag="nonexistent")
        assert len(no_match_tasks) == 0

    def test_filter_with_none_values(self):
        """Test filtering when passing None values (should not filter by that criterion)"""
        todo_manager = TodoManager()
        
        # Add tasks
        todo_manager.add_task(title="High Priority Task", description="Important", priority="High", tags={"work"})
        todo_manager.add_task(title="Low Priority Task", description="Less important", priority="Low", tags={"personal"})
        
        # Filter with None for priority (should not filter by priority)
        all_tasks = todo_manager.filter_tasks(priority=None)
        assert len(all_tasks) == 2
        
        # Filter with None for tag (should not filter by tag)
        all_tasks = todo_manager.filter_tasks(tag=None)
        assert len(all_tasks) == 2
        
        # Filter with None for status (should not filter by status)
        all_tasks = todo_manager.filter_tasks(status=None)
        assert len(all_tasks) == 2