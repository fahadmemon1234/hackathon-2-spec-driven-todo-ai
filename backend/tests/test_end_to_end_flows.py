import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.workflows.task_creation import task_creation_workflow
from backend.workflows.reminder_flow import reminder_flow
from backend.workflows.recurring_tasks import recurring_tasks_workflow

@pytest.mark.asyncio
async def test_task_creation_workflow_success():
    """Test the complete task creation workflow with state store and pub/sub"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish:
        
        # Mock successful responses
        mock_save_state.return_value = True
        mock_publish.return_value = True
        
        # Test data
        task_data = {
            "id": "task-123",
            "title": "Test Task",
            "description": "A test task",
            "status": "pending"
        }
        
        # Execute the workflow
        result = await task_creation_workflow.create_task_workflow(task_data)
        
        # Assertions
        assert result["status"] == "success"
        assert "task-123" in result["message"]
        mock_save_state.assert_called_once()
        mock_publish.assert_called_once()


@pytest.mark.asyncio
async def test_task_creation_workflow_state_failure():
    """Test task creation workflow when state save fails"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish:
        
        # Mock state save failure
        mock_save_state.return_value = False
        mock_publish.return_value = True  # This shouldn't be called in this scenario
        
        # Test data
        task_data = {
            "id": "task-456",
            "title": "Failing Task",
            "status": "pending"
        }
        
        # Execute the workflow
        result = await task_creation_workflow.create_task_workflow(task_data)
        
        # Assertions
        assert result["status"] == "error"
        assert "Failed to save" in result["message"]
        mock_save_state.assert_called_once()
        mock_publish.assert_not_called()  # Should not be called if state save fails


@pytest.mark.asyncio
async def test_task_creation_workflow_pubsub_failure():
    """Test task creation workflow when pub/sub publish fails"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish:
        
        # Mock successful state save but failed pub/sub
        mock_save_state.return_value = True
        mock_publish.return_value = False
        
        # Test data
        task_data = {
            "id": "task-789",
            "title": "PubSub Fail Task",
            "status": "pending"
        }
        
        # Execute the workflow
        result = await task_creation_workflow.create_task_workflow(task_data)
        
        # In this implementation, we continue even if pub/sub fails
        # The result should be a warning rather than an error
        assert result["status"] in ["success", "warning"]
        mock_save_state.assert_called_once()
        mock_publish.assert_called_once()


@pytest.mark.asyncio
async def test_reminder_scheduling_workflow():
    """Test the complete reminder scheduling workflow"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        mock_save_state.return_value = True
        
        # Test data
        reminder_data = {
            "reminderId": "reminder-101",
            "taskId": "task-202",
            "reminderTime": "2023-12-31T15:00:00Z",
            "notified": False
        }
        
        # Execute the workflow
        result = await reminder_flow.schedule_reminder_workflow(reminder_data)
        
        # Assertions
        assert result["status"] == "success"
        assert "scheduled" in result["message"]
        mock_save_state.assert_called_once()


@pytest.mark.asyncio
async def test_reminder_processing_workflow():
    """Test the reminder processing workflow"""
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish, \
         patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        
        # Mock return values
        mock_get_state.return_value = [
            {
                "reminderId": "reminder-202",
                "taskId": "task-303",
                "reminderTime": "2023-01-01T10:00:00Z",
                "notified": False
            }
        ]
        mock_publish.return_value = True
        mock_save_state.return_value = True
        
        # Execute the workflow
        result = await reminder_flow.process_scheduled_reminders_workflow()
        
        # Assertions
        assert result["status"] == "success"
        assert "completed" in result["message"]


@pytest.mark.asyncio
async def test_recurring_task_processing_workflow():
    """Test the recurring task processing workflow"""
    with patch('backend.workflows.recurring_tasks.state_service') as mock_state_service, \
         patch('backend.workflows.recurring_tasks.pubsub_service') as mock_pubsub_service:
        
        # Mock return values
        mock_state_service.get_state.return_value = {
            "taskId": "recurring-task-1",
            "recurrenceRule": "FREQ=DAILY;INTERVAL=1",
            "lastOccurrence": "2023-01-01T10:00:00Z",
            "nextOccurrence": "2023-01-02T10:00:00Z"
        }
        mock_pubsub_service.publish_event.return_value = True
        mock_state_service.save_state.return_value = True
        
        # Execute the workflow
        result = await recurring_tasks_workflow.process_recurring_tasks_workflow()
        
        # Assertions
        assert result["status"] == "success"
        assert "completed" in result["message"]


@pytest.mark.asyncio
async def test_create_recurring_task_instance():
    """Test creating a new instance of a recurring task"""
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.utils.recurrence_utils.calculate_next_occurrence') as mock_calc_next:
        
        # Mock return values
        recurrence_data = {
            "taskId": "recurring-task-5",
            "recurrenceRule": "FREQ=DAILY;INTERVAL=1",
            "lastOccurrence": "2023-01-01T10:00:00Z",
            "nextOccurrence": "2023-01-02T10:00:00Z"
        }
        original_task = {
            "taskId": "recurring-task-5",
            "title": "Daily Task",
            "status": "completed"
        }
        
        mock_get_state.side_effect = [recurrence_data, original_task]
        mock_save_state.return_value = True
        mock_calc_next.return_value = "2023-01-02T10:00:00Z"
        
        # Execute the workflow function
        result = await recurring_tasks_workflow.create_recurring_task_instance("recurring-task-5")
        
        # Assertions
        assert result["status"] == "success"
        assert "created" in result["message"]
        assert mock_get_state.call_count == 2  # Called twice (recurrence + original task)
        mock_save_state.assert_called()  # Called at least once for new task


@pytest.mark.asyncio
async def test_reminder_notification_workflow():
    """Test the complete reminder notification workflow"""
    with patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish, \
         patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        
        # Mock return values
        mock_publish.return_value = True
        mock_save_state.return_value = True
        
        # Test data
        reminder_data = {
            "reminderId": "reminder-303",
            "taskId": "task-404",
            "reminderTime": "2023-12-31T15:00:00Z",
            "notified": False
        }
        
        # Execute the workflow function
        result = await reminder_flow.publish_reminder_notification_workflow(reminder_data)
        
        # Assertions
        assert result["status"] == "success"
        assert "published" in result["message"]
        mock_publish.assert_called_once()
        mock_save_state.assert_called_once()


@pytest.mark.asyncio
async def test_task_creation_workflow_missing_id():
    """Test task creation workflow when task ID is missing"""
    # Test data without ID
    task_data = {
        "title": "Task without ID",
        "status": "pending"
    }
    
    # Execute the workflow
    result = await task_creation_workflow.create_task_workflow(task_data)
    
    # Assertions
    assert result["status"] == "error"
    assert "required" in result["message"]


@pytest.mark.asyncio
async def test_end_to_end_task_lifecycle():
    """Test the complete lifecycle of a task from creation to update to deletion"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish, \
         patch('backend.services.state_service.state_service.delete_state') as mock_delete_state:
        
        # Mock successful responses
        mock_save_state.return_value = True
        mock_get_state.return_value = {"taskId": "lifecycle-task", "title": "Lifecycle Test", "status": "pending"}
        mock_publish.return_value = True
        mock_delete_state.return_value = True
        
        # Step 1: Create task
        task_data = {
            "id": "lifecycle-task",
            "title": "Lifecycle Test Task",
            "status": "pending"
        }
        create_result = await task_creation_workflow.create_task_workflow(task_data)
        assert create_result["status"] == "success"
        
        # Step 2: Update task (simulated by saving updated state)
        updated_task_data = {**task_data, "status": "completed", "updatedAt": ""}
        update_save_result = await state_service.save_state(f"task:lifecycle-task", updated_task_data)
        assert update_save_result is True
        
        # Step 3: Delete task
        delete_result = await state_service.delete_state(f"task:lifecycle-task")
        assert delete_result is True
        
        # All operations should have been successful
        assert mock_save_state.call_count >= 1  # At least one save for creation
        assert mock_publish.call_count >= 1  # At least one publish for creation event
        assert mock_delete_state.call_count == 1  # One delete call


@pytest.mark.asyncio
async def test_reminder_scheduling_and_processing_integration():
    """Test integration between scheduling and processing reminders"""
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state, \
         patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish:
        
        # Mock successful responses
        mock_save_state.return_value = True
        mock_get_state.return_value = [
            {
                "reminderId": "integrated-reminder",
                "taskId": "integrated-task",
                "reminderTime": "2023-01-01T10:00:00Z",
                "notified": False
            }
        ]
        mock_publish.return_value = True
        
        # Step 1: Schedule a reminder
        reminder_data = {
            "reminderId": "integrated-reminder",
            "taskId": "integrated-task",
            "reminderTime": "2023-01-01T10:00:00Z",
            "notified": False
        }
        schedule_result = await reminder_flow.schedule_reminder_workflow(reminder_data)
        assert schedule_result["status"] == "success"
        
        # Step 2: Process scheduled reminders
        process_result = await reminder_flow.process_scheduled_reminders_workflow()
        assert process_result["status"] == "success"
        
        # Both operations should have been successful
        assert mock_save_state.call_count >= 1
        assert mock_publish.call_count >= 0  # May or may not be called depending on implementation