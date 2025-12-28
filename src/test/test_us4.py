"""
Tests for User Story 4: Search Tasks
"""

import pytest
from src.models.task import Task
from src.services.todo_manager import TodoManager


class TestUserStory4:
    """Test class for User Story 4: Search Tasks"""

    def test_search_by_title(self):
        """Test searching tasks by keyword in title"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Finish report", description="Complete the quarterly report", tags={"work", "important"})
        todo_manager.add_task(title="Call plumber", description="Fix the leaky faucet", tags={"home", "urgent"})
        
        # Search for "groceries"
        results = todo_manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"
        
        # Search for "report"
        results = todo_manager.search_tasks("report")
        assert len(results) == 1
        assert results[0].title == "Finish report"

    def test_search_by_description(self):
        """Test searching tasks by keyword in description"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Finish report", description="Complete the quarterly report", tags={"work", "important"})
        todo_manager.add_task(title="Call plumber", description="Fix the leaky faucet", tags={"home", "urgent"})
        
        # Search for "milk" in description
        results = todo_manager.search_tasks("milk")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"
        
        # Search for "leaky" in description
        results = todo_manager.search_tasks("leaky")
        assert len(results) == 1
        assert results[0].title == "Call plumber"

    def test_search_by_tags(self):
        """Test searching tasks by keyword in tags"""
        todo_manager = TodoManager()
        
        # Add some tasks with tags
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Finish report", description="Complete the quarterly report", tags={"work", "important"})
        todo_manager.add_task(title="Call plumber", description="Fix the leaky faucet", tags={"home", "urgent"})
        
        # Search for "shopping" in tags
        results = todo_manager.search_tasks("shopping")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"
        
        # Search for "work" in tags
        results = todo_manager.search_tasks("work")
        assert len(results) == 1
        assert results[0].title == "Finish report"

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        todo_manager = TodoManager()
        
        # Add a task
        todo_manager.add_task(title="Buy Groceries", description="Get Milk and Bread", tags={"Shopping", "Food"})
        
        # Search with different cases
        results = todo_manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Buy Groceries"
        
        results = todo_manager.search_tasks("GROCERIES")
        assert len(results) == 1
        assert results[0].title == "Buy Groceries"
        
        results = todo_manager.search_tasks("milk")
        assert len(results) == 1
        assert results[0].description == "Get Milk and Bread"
        
        results = todo_manager.search_tasks("SHOPPING")
        assert len(results) == 1
        assert "Shopping" in results[0].tags

    def test_search_multiple_matches(self):
        """Test searching when multiple tasks match the keyword"""
        todo_manager = TodoManager()
        
        # Add tasks with similar content
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Milk delivery", description="Schedule milk delivery", tags={"shopping", "dairy"})
        todo_manager.add_task(title="Finish report", description="Complete the quarterly report", tags={"work", "important"})
        
        # Search for "milk" - should match 2 tasks
        results = todo_manager.search_tasks("milk")
        assert len(results) == 2
        titles = {task.title for task in results}
        assert titles == {"Buy groceries", "Milk delivery"}

    def test_search_partial_matches(self):
        """Test searching with partial keyword matches"""
        todo_manager = TodoManager()
        
        # Add tasks
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Finish quarterly report", description="Complete the quarterly report", tags={"work", "important"})
        
        # Search for partial matches
        results = todo_manager.search_tasks("quarter")
        assert len(results) == 1
        assert results[0].title == "Finish quarterly report"

    def test_search_no_matches(self):
        """Test searching when no tasks match the keyword"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        todo_manager.add_task(title="Finish report", description="Complete the quarterly report", tags={"work", "important"})
        
        # Search for a keyword that doesn't exist
        results = todo_manager.search_tasks("nonexistent")
        assert len(results) == 0
        
        # Search for empty string
        results = todo_manager.search_tasks("")
        assert len(results) == 0

    def test_search_special_characters(self):
        """Test searching with special characters"""
        todo_manager = TodoManager()
        
        # Add tasks with special characters
        todo_manager.add_task(title="Fix bug #123", description="Resolve issue with login", tags={"bug", "urgent"})
        todo_manager.add_task(title="Update API", description="API changes for v2.0", tags={"api", "update"})
        
        # Search for special characters
        results = todo_manager.search_tasks("#123")
        assert len(results) == 1
        assert results[0].title == "Fix bug #123"
        
        results = todo_manager.search_tasks("v2.0")
        assert len(results) == 1
        assert results[0].description == "API changes for v2.0"

    def test_search_with_all_fields(self):
        """Test searching when keyword appears in title, description, and tags of the same task"""
        todo_manager = TodoManager()
        
        # Add a task where the keyword appears in multiple fields
        todo_manager.add_task(
            title="Work on API documentation", 
            description="Create documentation for the new API", 
            tags={"api", "documentation", "work"}
        )
        
        # Search for "api" - should match in title, description, and tags
        results = todo_manager.search_tasks("api")
        assert len(results) == 1
        task = results[0]
        assert "api" in task.title.lower()
        assert "api" in task.description.lower()
        assert "api" in {tag.lower() for tag in task.tags}

    def test_search_empty_keyword(self):
        """Test searching with an empty keyword"""
        todo_manager = TodoManager()
        
        # Add some tasks
        todo_manager.add_task(title="Buy groceries", description="Get milk and bread", tags={"shopping", "food"})
        
        # Search for empty string
        results = todo_manager.search_tasks("")
        assert len(results) == 0