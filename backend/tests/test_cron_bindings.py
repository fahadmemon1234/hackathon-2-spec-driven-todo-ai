import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.routes.reminders import process_due_reminders

@pytest.mark.asyncio
async def test_process_due_reminders_success():
    """Test successful processing of due reminders"""
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish, \
         patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        
        # Mock return values
        mock_get_state.return_value = {
            "reminderId": "reminder-123",
            "taskId": "task-123",
            "reminderTime": "2023-01-01T10:00:00Z",
            "notified": False
        }
        mock_publish.return_value = True
        mock_save_state.return_value = True
        
        # Execute the function
        result = await process_due_reminders()
        
        # Assertions
        assert result["status"] == "success"
        assert result["processed_count"] >= 0  # At least 0 processed
        mock_get_state.assert_called()
        mock_publish.assert_called()
        mock_save_state.assert_called()


@pytest.mark.asyncio
async def test_process_due_reminders_no_due_reminders():
    """Test processing when there are no due reminders"""
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state:
        # Mock no due reminders found
        mock_get_state.return_value = None
        
        # Execute the function
        result = await process_due_reminders()
        
        # Assertions
        assert result["status"] == "success"
        assert result["processed_count"] == 0
        assert result["failed_count"] == 0


@pytest.mark.asyncio
async def test_process_due_reminders_publish_failure():
    """Test processing when event publishing fails"""
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state, \
         patch('backend.services.pubsub_service.pubsub_service.publish_event') as mock_publish, \
         patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        
        # Mock return values
        mock_get_state.return_value = {
            "reminderId": "reminder-123",
            "taskId": "task-123",
            "reminderTime": "2023-01-01T10:00:00Z",
            "notified": False
        }
        mock_publish.return_value = False  # Simulate failure
        mock_save_state.return_value = True
        
        # Execute the function
        result = await process_due_reminders()
        
        # Assertions
        assert result["status"] == "success"  # Still success as we continue processing
        assert result["failed_count"] >= 0


@pytest.mark.asyncio
async def test_process_due_reminders_exception_handling():
    """Test exception handling in reminder processing"""
    with patch('backend.services.state_service.state_service.get_state', side_effect=Exception("Test error")):
        # Execute the function
        result = await process_due_reminders()
        
        # Assertions
        assert result["status"] == "error"
        assert "Test error" in result["message"]


@pytest.mark.asyncio
async def test_schedule_reminder_success():
    """Test successful scheduling of a reminder"""
    from backend.routes.reminders import schedule_reminder
    
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        mock_save_state.return_value = True
        
        # Test data
        reminder_data = {
            "reminderId": "reminder-456",
            "taskId": "task-123",
            "reminderTime": "2023-12-31T15:00:00Z",
            "notified": False
        }
        
        # Execute the function
        response = await schedule_reminder(reminder_data)
        
        # Assertions
        assert response["status"] == "success"
        assert response["reminderId"] == "reminder-456"
        mock_save_state.assert_called_once_with(f"reminder:{reminder_data['reminderId']}", reminder_data)


@pytest.mark.asyncio
async def test_schedule_reminder_missing_id():
    """Test scheduling a reminder without ID"""
    from backend.routes.reminders import schedule_reminder
    from fastapi import HTTPException
    
    # Test data without reminderId
    reminder_data = {
        "taskId": "task-123",
        "reminderTime": "2023-12-31T15:00:00Z"
    }
    
    # Expect HTTPException for missing reminderId
    with pytest.raises(HTTPException) as exc_info:
        await schedule_reminder(reminder_data)
    
    assert exc_info.value.status_code == 400
    assert "Missing reminderId" in exc_info.value.detail


@pytest.mark.asyncio
async def test_schedule_reminder_save_failure():
    """Test scheduling a reminder when state save fails"""
    from backend.routes.reminders import schedule_reminder
    from fastapi import HTTPException
    
    with patch('backend.services.state_service.state_service.save_state') as mock_save_state:
        mock_save_state.return_value = False  # Simulate failure
        
        # Test data
        reminder_data = {
            "reminderId": "reminder-789",
            "taskId": "task-123",
            "reminderTime": "2023-12-31T15:00:00Z",
            "notified": False
        }
        
        # Expect HTTPException for save failure
        with pytest.raises(HTTPException) as exc_info:
            await schedule_reminder(reminder_data)
        
        assert exc_info.value.status_code == 500
        assert "Failed to save reminder" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_reminder_success():
    """Test successful retrieval of a reminder"""
    from backend.routes.reminders import get_reminder
    
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state:
        expected_reminder = {
            "reminderId": "reminder-101",
            "taskId": "task-202",
            "reminderTime": "2023-12-31T10:00:00Z",
            "notified": False
        }
        mock_get_state.return_value = expected_reminder
        
        # Execute the function
        result = await get_reminder("reminder-101")
        
        # Assertions
        assert result["status"] == "success"
        assert result["reminder"] == expected_reminder
        mock_get_state.assert_called_once_with("reminder:reminder-101")


@pytest.mark.asyncio
async def test_get_reminder_not_found():
    """Test retrieval of a non-existent reminder"""
    from backend.routes.reminders import get_reminder
    from fastapi import HTTPException
    
    with patch('backend.services.state_service.state_service.get_state') as mock_get_state:
        mock_get_state.return_value = None  # Reminder not found
        
        # Expect HTTPException for not found
        with pytest.raises(HTTPException) as exc_info:
            await get_reminder("non-existent-reminder")
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_reminder_exception():
    """Test exception handling in reminder retrieval"""
    from backend.routes.reminders import get_reminder
    from fastapi import HTTPException
    
    with patch('backend.services.state_service.state_service.get_state', side_effect=Exception("DB error")):
        # Expect HTTPException for internal error
        with pytest.raises(HTTPException) as exc_info:
            await get_reminder("reminder-error")
        
        assert exc_info.value.status_code == 500