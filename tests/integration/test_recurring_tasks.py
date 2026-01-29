"""
Integration tests for recurring task functionality.
"""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from sqlmodel import Session, select
from models import Task
from utils.recurrence_utils import convert_ui_recurrence_options_to_rrule


def test_create_daily_recurring_task(client, db_session, authenticated_headers):
    """Test creating a daily recurring task."""
    # Prepare test data
    recurrence_rule = convert_ui_recurrence_options_to_rrule(
        frequency="daily",
        interval=1
    )
    
    task_data = {
        "title": "Daily recurring task",
        "description": "This is a daily recurring task",
        "is_recurring": True,
        "recurrence_rule": recurrence_rule,
        "due_date": datetime.now().isoformat()
    }
    
    # Make request to create task
    response = client.post("/tasks", json=task_data, headers=authenticated_headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Daily recurring task"
    assert data["is_recurring"] is True
    assert data["recurrence_rule"] == recurrence_rule


def test_complete_recurring_task_creates_next_instance(client, db_session, authenticated_headers):
    """Test that completing a recurring task creates the next instance."""
    # Create a recurring task first
    recurrence_rule = convert_ui_recurrence_options_to_rrule(
        frequency="daily",
        interval=1
    )
    
    task_data = {
        "title": "Test recurring task",
        "is_recurring": True,
        "recurrence_rule": recurrence_rule,
        "due_date": datetime.now().isoformat()
    }
    
    response = client.post("/tasks", json=task_data, headers=authenticated_headers)
    assert response.status_code == 200
    
    created_task = response.json()
    task_id = created_task["id"]
    
    # Verify the task was created
    response = client.get(f"/tasks/{task_id}", headers=authenticated_headers)
    assert response.status_code == 200
    
    # Complete the task (this should trigger creation of next instance)
    response = client.patch(f"/tasks/{task_id}/complete", headers=authenticated_headers)
    assert response.status_code == 200
    
    completed_task = response.json()
    assert completed_task["completed"] is True


def test_recurring_task_with_end_after_count(client, db_session, authenticated_headers):
    """Test recurring task with end after count condition."""
    recurrence_rule = convert_ui_recurrence_options_to_rrule(
        frequency="daily",
        interval=1,
        end_type="after",
        end_after_count=3
    )
    
    task_data = {
        "title": "Recurring task with end count",
        "is_recurring": True,
        "recurrence_rule": recurrence_rule,
        "recurrence_max_count": 3,
        "due_date": datetime.now().isoformat()
    }
    
    response = client.post("/tasks", json=task_data, headers=authenticated_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_recurring"] is True
    assert data["recurrence_max_count"] == 3


def test_recurring_task_with_end_date(client, db_session, authenticated_headers):
    """Test recurring task with end date condition."""
    from datetime import timedelta
    
    end_date = datetime.now() + timedelta(days=7)
    recurrence_rule = convert_ui_recurrence_options_to_rrule(
        frequency="daily",
        interval=1,
        end_type="on",
        end_date=end_date
    )
    
    task_data = {
        "title": "Recurring task with end date",
        "is_recurring": True,
        "recurrence_rule": recurrence_rule,
        "recurrence_end_date": end_date.isoformat(),
        "due_date": datetime.now().isoformat()
    }
    
    response = client.post("/tasks", json=task_data, headers=authenticated_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_recurring"] is True
    assert data["recurrence_end_date"] is not None


def test_non_recurring_task_completion_normal_behavior(client, db_session, authenticated_headers):
    """Test that non-recurring tasks behave normally when completed."""
    task_data = {
        "title": "Non-recurring task",
        "is_recurring": False,
        "due_date": datetime.now().isoformat()
    }
    
    response = client.post("/tasks", json=task_data, headers=authenticated_headers)
    assert response.status_code == 200
    
    created_task = response.json()
    task_id = created_task["id"]
    assert created_task["is_recurring"] is False
    
    # Complete the task
    response = client.patch(f"/tasks/{task_id}/complete", headers=authenticated_headers)
    assert response.status_code == 200
    
    completed_task = response.json()
    assert completed_task["completed"] is True
    
    # Verify no additional tasks were created for non-recurring task
    all_tasks_response = client.get("/tasks", headers=authenticated_headers)
    all_tasks = all_tasks_response.json()
    non_recurring_tasks = [task for task in all_tasks if task["title"] == "Non-recurring task"]
    assert len(non_recurring_tasks) == 1  # Should only be the original task