import pytest
from unittest.mock import Mock, patch
from src.cli.main import TodoApp
from src.services.todo_manager import TodoManager


def test_add_command_integration():
    """Test the integration of the 'add' command from CLI to business logic."""
    app = TodoApp()

    # Process the add command
    app.process_command("add Buy milk Grocery shopping")

    # Check that the task was added to the manager
    tasks = app.todo_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].description == "Grocery shopping"
    assert tasks[0].completed is False
    assert tasks[0].priority == "Medium"  # Default priority


def test_add_command_output():
    """Test that the 'add' command produces the correct output."""
    app = TodoApp()

    # Capture the output of the add command
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command("add Buy milk Grocery shopping")

    output = f.getvalue().strip()
    assert "[SUCCESS] Task added with ID:" in output
    assert "Buy milk" in output

    # Verify the task was actually added
    tasks = app.todo_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].description == "Grocery shopping"


def test_add_command_validation_error():
    """Test that the 'add' command handles validation errors correctly."""
    app = TodoApp()

    # Capture the output when validation fails
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command("add " + "A"*101 + " Description")  # Title too long

    output = f.getvalue().strip()
    assert "[ERROR]" in output
    assert "Title must be between 1 and 100 characters" in output


def test_list_command_integration():
    """Test the integration of the 'list' command from CLI to business logic."""
    app = TodoApp()

    # Add a task first
    app.process_command("add Buy milk Grocery shopping")

    # Capture the output of the list command
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command("list")

    output = f.getvalue().strip()
    assert "Buy milk" in output
    assert "Grocery shopping" in output
    assert "[INCOMPLETE]" in output


def test_list_command_empty():
    """Test that the 'list' command handles empty task list correctly."""
    app = TodoApp()

    # Capture the output when there are no tasks
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command("list")

    output = f.getvalue().strip()
    assert "No tasks found." in output


def test_complete_command_integration():
    """Test the integration of the 'complete' command from CLI to business logic."""
    app = TodoApp()

    # Add a task first
    app.process_command("add Buy milk Grocery shopping")

    # Get the task to verify its initial state
    tasks = app.todo_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is False

    # Complete the task
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command(f"complete {tasks[0].id}")

    output = f.getvalue().strip()
    assert f"Task {tasks[0].id} marked as complete" in output

    # Verify the task is now complete
    tasks = app.todo_manager.get_all_tasks()
    assert tasks[0].completed is True


def test_incomplete_command_integration():
    """Test the integration of the 'incomplete' command from CLI to business logic."""
    app = TodoApp()

    # Add and complete a task first
    app.process_command("add Buy milk Grocery shopping")
    tasks = app.todo_manager.get_all_tasks()
    task_id = tasks[0].id
    app.todo_manager.mark_complete(task_id)

    # Verify the task is initially complete
    tasks = app.todo_manager.get_all_tasks()
    assert tasks[0].completed is True

    # Mark the task as incomplete
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command(f"incomplete {task_id}")

    output = f.getvalue().strip()
    assert f"Task {task_id} marked as incomplete" in output

    # Verify the task is now incomplete
    tasks = app.todo_manager.get_all_tasks()
    assert tasks[0].completed is False


def test_update_command_integration():
    """Test the integration of the 'update' command from CLI to business logic."""
    app = TodoApp()

    # Add a task first
    app.process_command("add Buy milk Grocery shopping")
    tasks = app.todo_manager.get_all_tasks()
    task_id = tasks[0].id

    # Verify initial values
    assert tasks[0].title == "Buy milk"
    assert tasks[0].description == "Grocery shopping"

    # Update the task
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command(f"update {task_id} --title \"Buy bread\" --description \"Bakery items\"")

    output = f.getvalue().strip()
    assert f"Task {task_id} updated successfully" in output

    # Verify updated values
    updated_task = app.todo_manager.get_task_by_id(task_id)
    assert updated_task.title == "Buy bread"
    assert updated_task.description == "Bakery items"


def test_update_command_validation_error():
    """Test that the 'update' command handles validation errors correctly."""
    app = TodoApp()

    # Add a task first
    app.process_command("add Buy milk Grocery shopping")
    tasks = app.todo_manager.get_all_tasks()
    task_id = tasks[0].id

    # Try to update with invalid title (too long)
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command(f"update {task_id} --title " + "\"" + "A"*101 + "\"")

    output = f.getvalue().strip()
    assert "[ERROR]" in output
    assert "Title must be between 1 and 100 characters" in output


def test_delete_command_integration():
    """Test the integration of the 'delete' command from CLI to business logic."""
    app = TodoApp()

    # Add a task first
    app.process_command("add Buy milk Grocery shopping")
    tasks = app.todo_manager.get_all_tasks()
    assert len(tasks) == 1
    task_id = tasks[0].id

    # Delete the task
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command(f"delete {task_id}")

    output = f.getvalue().strip()
    assert f"Task {task_id} deleted successfully" in output

    # Verify the task is gone
    tasks = app.todo_manager.get_all_tasks()
    assert len(tasks) == 0


def test_delete_command_nonexistent_task():
    """Test that the 'delete' command handles non-existent task IDs correctly."""
    app = TodoApp()

    # Try to delete a non-existent task
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        app.process_command("delete 999")

    output = f.getvalue().strip()
    assert "Task with ID 999 does not exist." in output